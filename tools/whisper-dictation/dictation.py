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
import io
import json
import sys
import tempfile
import threading
import time
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


class DictationApp:
    def __init__(self, config: dict):
        self.config = config
        self.recording = False
        self.audio_frames = []
        self.stream = None
        self._lock = threading.Lock()

    def start(self):
        """Inicia o app de dictation."""
        hotkey = self.config["hotkey"]
        print(f"Whisper Dictation ativo.")
        print(f"  Hotkey: {hotkey}")
        print(f"  Idioma: {self.config['language']}")
        print(f"  Aperte {hotkey} para gravar. Aperte de novo para transcrever.")
        print(f"  Ctrl+C para sair.")
        print()

        keyboard.add_hotkey(hotkey, self._toggle_recording)

        try:
            keyboard.wait()
        except KeyboardInterrupt:
            self._cleanup()
            print("\nDictation encerrado.")

    def _toggle_recording(self):
        """Alterna entre gravação e transcrição."""
        with self._lock:
            if not self.recording:
                self._start_recording()
            else:
                self._stop_and_transcribe()

    def _start_recording(self):
        """Começa a gravar do microfone."""
        self.recording = True
        self.audio_frames = []

        sample_rate = self.config["sample_rate"]
        channels = self.config["channels"]

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"  [audio] {status}", file=sys.stderr)
            self.audio_frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype="int16",
            callback=audio_callback,
        )
        self.stream.start()
        print("  [REC] Gravando... (aperte hotkey para parar)")

    def _stop_and_transcribe(self):
        """Para a gravação, transcreve e cola o texto."""
        self.recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.audio_frames:
            print("  [!] Nenhum áudio capturado.")
            return

        print("  [...] Transcrevendo...")

        # Salvar áudio em WAV temporário
        audio_data = np.concatenate(self.audio_frames, axis=0)
        temp_path = Path(tempfile.gettempdir()) / "whisper_dictation_temp.wav"

        wavfile.write(str(temp_path), self.config["sample_rate"], audio_data)

        try:
            text = transcribe_audio(
                str(temp_path),
                language=self.config["language"],
            )

            if text.strip():
                pyperclip.copy(text)
                # Pequeno delay para garantir que o clipboard atualizou
                time.sleep(0.05)
                keyboard.send("ctrl+v")
                print(f"  [OK] \"{text}\"")
            else:
                print("  [!] Transcrição vazia.")

        except Exception as e:
            print(f"  [ERRO] {e}", file=sys.stderr)

        finally:
            # Limpar arquivo temporário
            temp_path.unlink(missing_ok=True)

    def _cleanup(self):
        """Limpa recursos."""
        if self.stream:
            self.stream.stop()
            self.stream.close()


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
