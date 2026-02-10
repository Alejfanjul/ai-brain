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
import os
import sys
import tempfile
import threading
import time
from enum import Enum, auto
from pathlib import Path

import keyboard
import numpy as np
import pyperclip
import sounddevice as sd
from scipy.io import wavfile

from transcribe import transcribe_audio

# Configuração padrão
DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "language": "pt",
    "sample_rate": 16000,
    "channels": 1,
}


class AppState(Enum):
    IDLE = auto()
    RECORDING = auto()
    PROCESSING = auto()
    SUCCESS = auto()
    ERROR = auto()


class DictationApp:
    def __init__(self, config: dict, on_state_change=None):
        self.config = config
        self._state = AppState.IDLE
        self._on_state_change = on_state_change
        self._audio_frames = []
        self._audio_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self.stream = None

    def _set_state(self, new_state: AppState):
        self._state = new_state
        if self._on_state_change:
            try:
                self._on_state_change(new_state)
            except Exception:
                pass

    def preflight_checks(self) -> list[str]:
        """Verifica pré-requisitos. Retorna lista de erros (vazia = tudo OK)."""
        errors = []

        if not os.environ.get("OPENAI_API_KEY"):
            errors.append("OPENAI_API_KEY não configurada")

        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d["max_input_channels"] > 0]
            if not input_devices:
                errors.append("Nenhum microfone encontrado")
        except Exception as e:
            errors.append(f"Erro ao verificar microfone: {e}")

        try:
            pyperclip.copy("test")
            pyperclip.paste()
        except Exception as e:
            errors.append(f"Clipboard não acessível: {e}")

        return errors

    def toggle_recording(self):
        """Alterna entre gravação e transcrição."""
        with self._state_lock:
            if self._state == AppState.IDLE:
                self._start_recording()
            elif self._state == AppState.RECORDING:
                self._set_state(AppState.PROCESSING)
                self._stop_stream()
                threading.Thread(
                    target=self._transcribe_and_paste,
                    daemon=True,
                ).start()
            # PROCESSING, SUCCESS, ERROR → ignora F9

    def _start_recording(self):
        """Começa a gravar do microfone."""
        with self._audio_lock:
            self._audio_frames = []

        sample_rate = self.config["sample_rate"]
        channels = self.config["channels"]

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"  [audio] {status}", file=sys.stderr)
            with self._audio_lock:
                self._audio_frames.append(indata.copy())

        try:
            self.stream = sd.InputStream(
                samplerate=sample_rate,
                channels=channels,
                dtype="int16",
                callback=audio_callback,
            )
            self.stream.start()
            self._set_state(AppState.RECORDING)
            print("  [REC] Gravando... (aperte hotkey para parar)")
        except Exception as e:
            print(f"  [ERRO] Falha ao iniciar gravação: {e}", file=sys.stderr)
            self._set_state(AppState.ERROR)

    def _stop_stream(self):
        """Para o stream de áudio de forma segura."""
        if self.stream:
            try:
                self.stream.stop()
            except Exception:
                try:
                    self.stream.abort()
                except Exception:
                    pass
            try:
                self.stream.close()
            except Exception:
                pass
            self.stream = None

    def _collect_audio(self):
        """Coleta frames de áudio de forma thread-safe."""
        with self._audio_lock:
            frames = self._audio_frames.copy()
            self._audio_frames.clear()
        if not frames:
            return None
        return np.concatenate(frames, axis=0)

    def _paste_text(self, text: str) -> bool:
        """Cola texto via clipboard com retry."""
        pyperclip.copy(text)
        for _ in range(3):
            time.sleep(0.1)
            try:
                if pyperclip.paste() == text:
                    keyboard.send("ctrl+v")
                    return True
            except Exception:
                pass
        # Fallback: tenta colar mesmo sem verificação
        keyboard.send("ctrl+v")
        return False

    def _transcribe_and_paste(self):
        """Transcreve o áudio gravado e cola o texto. Roda em thread separada."""
        try:
            audio_data = self._collect_audio()

            if audio_data is None:
                print("  [!] Nenhum áudio capturado.")
                self._set_state(AppState.ERROR)
                return

            print("  [...] Transcrevendo...")

            temp_path = Path(tempfile.gettempdir()) / "whisper_dictation_temp.wav"
            wavfile.write(str(temp_path), self.config["sample_rate"], audio_data)

            try:
                text = transcribe_audio(
                    str(temp_path),
                    language=self.config["language"],
                )

                if text.strip():
                    self._paste_text(text)
                    print(f'  [OK] "{text}"')
                    self._set_state(AppState.SUCCESS)
                else:
                    print("  [!] Transcrição vazia.")
                    self._set_state(AppState.ERROR)

            except Exception as e:
                print(f"  [ERRO] {e}", file=sys.stderr)
                self._set_state(AppState.ERROR)

            finally:
                temp_path.unlink(missing_ok=True)

        except Exception as e:
            print(f"  [ERRO] Falha inesperada: {e}", file=sys.stderr)
            self._set_state(AppState.ERROR)

    def start(self):
        """Inicia o app de dictation (modo standalone, sem tray icon)."""
        hotkey = self.config["hotkey"]
        print("Whisper Dictation ativo.")
        print(f"  Hotkey: {hotkey}")
        print(f"  Idioma: {self.config['language']}")
        print(f"  Aperte {hotkey} para gravar. Aperte de novo para transcrever.")
        print("  Ctrl+C para sair.")
        print()

        keyboard.add_hotkey(hotkey, self.toggle_recording)

        try:
            keyboard.wait()
        except KeyboardInterrupt:
            self.cleanup()
            print("\nDictation encerrado.")

    def cleanup(self):
        """Limpa recursos."""
        self._stop_stream()


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
