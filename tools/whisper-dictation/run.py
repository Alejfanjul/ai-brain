"""
Whisper Dictation — Ponto de entrada principal.

Orquestra DictationApp (áudio + transcrição) com TrayManager (ícone no system tray).
Roda no Windows. Ponto de entrada para autostart e uso diário.

Uso:
    python run.py
    python run.py --hotkey F9
    python run.py --language en
"""

import argparse
import sys
import threading

import keyboard

from dictation import AppState, DictationApp, load_config
from tray import TrayManager

# Tempo em segundos para estados transitórios (SUCCESS/ERROR) antes de voltar a IDLE
TRANSIENT_STATE_DURATION = 2.0


def main():
    parser = argparse.ArgumentParser(description="Whisper Dictation")
    parser.add_argument("--hotkey", help="Hotkey para toggle (ex: F9, ctrl+shift+space)")
    parser.add_argument("--language", help="Idioma para transcrição (ex: pt, en)")
    args = parser.parse_args()

    config = load_config()
    if args.hotkey:
        config["hotkey"] = args.hotkey
    if args.language:
        config["language"] = args.language

    tray = TrayManager()

    def on_state_change(state: AppState):
        tray.update_state(state)
        # Estados transitórios voltam para IDLE automaticamente
        if state in (AppState.SUCCESS, AppState.ERROR):
            def reset():
                tray.update_state(AppState.IDLE)
            threading.Timer(TRANSIENT_STATE_DURATION, reset).start()

    app = DictationApp(config, on_state_change=on_state_change)

    # Pre-flight checks
    errors = app.preflight_checks()
    if errors:
        for e in errors:
            print(f"  [ERRO] {e}", file=sys.stderr)

    hotkey = config["hotkey"]
    print(f"Whisper Dictation ativo. Hotkey: {hotkey}")

    def setup(icon):
        """Roda quando o tray icon está pronto (thread separada do pystray)."""
        icon.visible = True
        keyboard.add_hotkey(hotkey, app.toggle_recording)
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            pass
        app.cleanup()
        icon.stop()

    # pystray.run() bloqueia a main thread (message pump do Windows)
    # setup() roda em thread separada gerenciada pelo pystray
    tray.run(setup_callback=setup, config=config)


if __name__ == "__main__":
    main()
