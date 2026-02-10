"""
Whisper Dictation — Speech-to-text com hotkey global.

Aperta hotkey para começar a gravar, aperta de novo para transcrever.
Texto transcrito é colado onde o cursor estiver.

Uso:
    python dictation.py
    python dictation.py --hotkey "ctrl+shift+space"
    python dictation.py --language en
"""

import argparse
import json
import logging
import os
import signal
import sys
import tempfile
import threading
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import keyboard
import numpy as np
import pyperclip
import sounddevice as sd
from scipy.io import wavfile

from transcribe import transcribe_audio

# --- Logging ---

LOG_DIR = Path(__file__).parent
LOG_FILE = LOG_DIR / "whisper_dictation.log"

logger = logging.getLogger("dictation")
logger.setLevel(logging.DEBUG)

# Arquivo: rotação 1MB, 2 backups
_file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=2, encoding="utf-8"
)
_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
)
logger.addHandler(_file_handler)

# Console: só quando não rodando minimizado
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_console_handler)


# --- Feedback sonoro ---
# Gera WAV em memória e toca via winsound.PlaySound (Windows audio system).
# Não usa sounddevice para output — evita conflito com InputStream ativo.

import io
import wave as wave_mod

BEEP_SAMPLE_RATE = 44100
_tone_cache: dict[tuple[int, int], bytes] = {}


def _make_wav(freq: int, duration_ms: int, volume: float = 0.5) -> bytes:
    """Gera WAV em memória com fade-in para compatibilidade Bluetooth.

    Bluetooth headphones entram em sleep quando não há áudio.
    O fade-in de 150ms "acorda" o dispositivo antes do tom principal.
    """
    key = (freq, duration_ms)
    if key in _tone_cache:
        return _tone_cache[key]

    primer_ms = 350  # tempo para acordar Bluetooth
    total_ms = primer_ms + duration_ms

    samples = int(BEEP_SAMPLE_RATE * total_ms / 1000)
    t = np.linspace(0, total_ms / 1000, samples, endpoint=False)
    wave = np.sin(2 * np.pi * freq * t) * volume

    # Fade-in ao longo do primer: volume sobe de 0 → 100%
    primer_samples = int(BEEP_SAMPLE_RATE * primer_ms / 1000)
    wave[:primer_samples] *= np.linspace(0, 1, primer_samples)

    data = (wave * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave_mod.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(BEEP_SAMPLE_RATE)
        wf.writeframes(data.tobytes())

    wav_bytes = buf.getvalue()
    _tone_cache[key] = wav_bytes
    return wav_bytes


def _tone(freq: int, duration_ms: int) -> None:
    """Toca tom pela saída de áudio do Windows — roda em thread separada."""
    def _play():
        try:
            import winsound
            wav = _make_wav(freq, duration_ms)
            winsound.PlaySound(wav, winsound.SND_MEMORY)
        except Exception as e:
            logger.debug(f"Beep falhou: {e}")

    threading.Thread(target=_play, daemon=True).start()


def beep_start_recording():
    _tone(400, 400)


def beep_stop_recording():
    _tone(800, 400)


def beep_success():
    _tone(1200, 500)


def beep_error():
    _tone(300, 700)


def beep_busy():
    _tone(600, 300)


# --- Singleton ---

LOCK_FILE = Path(tempfile.gettempdir()) / "whisper_dictation.lock"


def _kill_existing_instance() -> None:
    """Se outra instância está rodando, mata ela."""
    if not LOCK_FILE.exists():
        return

    try:
        pid = int(LOCK_FILE.read_text().strip())
        if pid == os.getpid():
            return
        os.kill(pid, signal.SIGTERM)
        logger.info(f"Instância anterior (PID {pid}) terminada.")
        time.sleep(0.5)  # Aguarda processo morrer
    except (ValueError, ProcessLookupError, PermissionError):
        pass  # PID inválido ou processo já morreu
    except OSError:
        pass

    LOCK_FILE.unlink(missing_ok=True)


def _acquire_lock() -> None:
    """Registra PID no lock file."""
    _kill_existing_instance()
    LOCK_FILE.write_text(str(os.getpid()))
    logger.info(f"Lock adquirido (PID {os.getpid()}).")


def _release_lock() -> None:
    """Remove lock file."""
    try:
        if LOCK_FILE.exists() and LOCK_FILE.read_text().strip() == str(os.getpid()):
            LOCK_FILE.unlink(missing_ok=True)
            logger.info("Lock liberado.")
    except OSError:
        pass


# --- Configuração ---

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "language": "pt",
    "sample_rate": 16000,
    "channels": 1,
}


# --- App ---

# Estados possíveis
STATE_READY = "ready"
STATE_RECORDING = "recording"
STATE_TRANSCRIBING = "transcribing"


class DictationApp:
    def __init__(self, config: dict):
        self.config = config
        self.state = STATE_READY
        self.audio_frames = []
        self.stream = None
        self._lock = threading.Lock()

    def start(self):
        """Inicia o app de dictation."""
        _acquire_lock()

        hotkey = self.config["hotkey"]
        logger.info("Whisper Dictation ativo.")
        logger.info(f"  Hotkey: {hotkey}")
        logger.info(f"  Idioma: {self.config['language']}")
        logger.info(f"  Log: {LOG_FILE}")
        logger.info(f"  Aperte {hotkey} para gravar. Aperte de novo para transcrever.")

        keyboard.add_hotkey(hotkey, self._toggle_recording)

        try:
            keyboard.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()
            _release_lock()
            logger.info("Dictation encerrado.")

    def _toggle_recording(self):
        """Alterna entre gravação e transcrição."""
        with self._lock:
            if self.state == STATE_READY:
                self._start_recording()
            elif self.state == STATE_RECORDING:
                self._stop_and_transcribe()
            elif self.state == STATE_TRANSCRIBING:
                logger.info("  [!] Transcrevendo... aguarde.")
                threading.Thread(target=beep_busy, daemon=True).start()

    def _start_recording(self):
        """Começa a gravar do microfone."""
        self.state = STATE_RECORDING
        self.audio_frames = []

        sample_rate = self.config["sample_rate"]
        channels = self.config["channels"]

        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"  [audio] {status}")
            self.audio_frames.append(indata.copy())

        try:
            self.stream = sd.InputStream(
                samplerate=sample_rate,
                channels=channels,
                dtype="int16",
                callback=audio_callback,
            )
            self.stream.start()
        except Exception as e:
            logger.error(f"  [ERRO] Falha ao abrir microfone: {e}")
            beep_error()
            self.state = STATE_READY
            return

        beep_start_recording()
        logger.info("  [REC] Gravando... (aperte hotkey para parar)")

    def _stop_and_transcribe(self):
        """Para a gravação e inicia transcrição em thread separada."""
        self.state = STATE_TRANSCRIBING

        # Para o stream imediatamente
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                logger.warning(f"  [audio] Erro ao fechar stream: {e}")
            self.stream = None

        if not self.audio_frames:
            logger.info("  [!] Nenhum áudio capturado.")
            beep_error()
            self.state = STATE_READY
            return

        beep_stop_recording()
        logger.info("  [...] Transcrevendo...")

        # Captura frames antes de passar pra thread
        frames = self.audio_frames.copy()
        self.audio_frames = []

        # Transcreve em thread separada — F9 continua responsivo
        thread = threading.Thread(
            target=self._transcribe_worker,
            args=(frames,),
            daemon=True,
        )
        thread.start()

    def _transcribe_worker(self, frames: list):
        """Worker que roda em thread: transcreve e cola texto."""
        temp_path = None
        try:
            # Salvar áudio em WAV temporário
            audio_data = np.concatenate(frames, axis=0)
            temp_path = Path(tempfile.gettempdir()) / f"whisper_dictation_{os.getpid()}.wav"
            wavfile.write(str(temp_path), self.config["sample_rate"], audio_data)

            # Transcrever com timeout e retry
            text = self._transcribe_with_retry(str(temp_path))

            if text and text.strip():
                pyperclip.copy(text)
                time.sleep(0.05)  # Aguarda clipboard sincronizar
                keyboard.send("ctrl+v")
                beep_success()
                logger.info(f'  [OK] "{text}"')
            else:
                logger.info("  [!] Transcrição vazia.")
                beep_error()

        except Exception as e:
            logger.error(f"  [ERRO] {e}")
            beep_error()

        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)
            self.state = STATE_READY

    def _transcribe_with_retry(self, audio_path: str, max_retries: int = 1) -> str:
        """Chama Whisper API com timeout e retry."""
        from openai import OpenAI

        client = OpenAI(timeout=30.0)

        for attempt in range(max_retries + 1):
            try:
                with open(audio_path, "rb") as f:
                    result = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,
                        language=self.config["language"],
                    )
                return result.text
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"  [RETRY] Tentativa {attempt + 1} falhou: {e}")
                    time.sleep(1)
                else:
                    raise

    def _cleanup(self):
        """Limpa recursos."""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass


def load_config() -> dict:
    """Carrega configuração do config.json ou usa defaults."""
    config_path = Path(__file__).parent / "config.json"

    config = DEFAULT_CONFIG.copy()

    if config_path.exists():
        with open(config_path) as f:
            user_config = json.load(f)
            config.update(user_config)

    return config


def main():
    parser = argparse.ArgumentParser(description="Whisper Dictation")
    parser.add_argument("--hotkey", help="Hotkey para toggle (ex: ctrl+shift+space)")
    parser.add_argument("--language", help="Idioma para transcrição (ex: pt, en)")
    args = parser.parse_args()

    config = load_config()

    if args.hotkey:
        config["hotkey"] = args.hotkey
    if args.language:
        config["language"] = args.language

    app = DictationApp(config)
    app.start()


if __name__ == "__main__":
    main()
