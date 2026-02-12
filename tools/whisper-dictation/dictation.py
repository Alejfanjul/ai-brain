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
import ctypes
import ctypes.wintypes as wintypes
import json
import logging
import os
import signal
import sys
import tempfile
import threading
import time
from enum import Enum, auto
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

_file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=2, encoding="utf-8"
)
_file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
)
logger.addHandler(_file_handler)

# pythonw.exe seta sys.stdout = None — só adiciona console handler se disponível
if sys.stdout is not None:
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(_console_handler)


# --- Estados ---


class AppState(Enum):
    IDLE = auto()
    RECORDING = auto()
    PROCESSING = auto()
    SUCCESS = auto()
    ERROR = auto()


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
        time.sleep(0.5)
    except (ValueError, ProcessLookupError, PermissionError):
        pass
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


# --- System Tray Icon ---
# Opcional: se pystray/pillow não estiver instalado, funciona sem ícone.

_tray_icon = None
_tray_available = False

try:
    import pystray
    from PIL import Image, ImageDraw

    _tray_available = True

    _TRAY_COLORS = {
        AppState.IDLE: "#808080",
        AppState.RECORDING: "#FF0000",
        AppState.PROCESSING: "#FFC800",
        AppState.SUCCESS: "#00CC00",
        AppState.ERROR: "#CC0000",
    }

    def _create_tray_image(color: str) -> Image.Image:
        """Cria ícone circular com a cor do estado."""
        size = 64
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([(4, 4), (60, 60)], fill=color, outline="#333333", width=2)
        return img

    # Cache de ícones pré-renderizados
    _tray_icons_cache: dict[AppState, Image.Image] = {}

    def _get_tray_image(state: AppState) -> Image.Image:
        if state not in _tray_icons_cache:
            _tray_icons_cache[state] = _create_tray_image(
                _TRAY_COLORS.get(state, "#808080")
            )
        return _tray_icons_cache[state]

    _TRAY_TOOLTIPS = {
        AppState.IDLE: "Whisper — Pronto (F9)",
        AppState.RECORDING: "Whisper — Gravando...",
        AppState.PROCESSING: "Whisper — Transcrevendo...",
        AppState.SUCCESS: "Whisper — Sucesso!",
        AppState.ERROR: "Whisper — Erro",
    }

    def _update_tray(state: AppState) -> None:
        """Atualiza ícone e tooltip do tray."""
        if _tray_icon is None:
            return
        _tray_icon.icon = _get_tray_image(state)
        _tray_icon.title = _TRAY_TOOLTIPS.get(state, "Whisper Dictation")

    def _flash_tray(state: AppState, duration: float = 2.0) -> None:
        """Flash temporário no tray (sucesso/erro), depois volta para idle."""
        if _tray_icon is None:
            return
        _update_tray(state)
        time.sleep(duration)
        _update_tray(AppState.IDLE)

    def _start_tray(on_quit_callback) -> None:
        """Inicia o tray icon em thread daemon."""
        global _tray_icon
        menu = pystray.Menu(
            pystray.MenuItem("Sair", lambda icon, item: on_quit_callback()),
        )
        _tray_icon = pystray.Icon(
            "whisper-dictation",
            icon=_get_tray_image(AppState.IDLE),
            title=_TRAY_TOOLTIPS[AppState.IDLE],
            menu=menu,
        )
        threading.Thread(target=_tray_icon.run, daemon=True).start()
        logger.info("  Tray icon ativo.")

    def _stop_tray() -> None:
        """Para o tray icon."""
        global _tray_icon
        if _tray_icon:
            _tray_icon.visible = False
            _tray_icon.stop()
            _tray_icon = None

except ImportError:
    logger.debug("pystray/pillow não instalado — tray icon desativado.")

    def _update_tray(state: AppState) -> None:
        pass

    def _flash_tray(state: AppState, duration: float = 2.0) -> None:
        pass

    def _start_tray(on_quit_callback) -> None:
        pass

    def _stop_tray() -> None:
        pass


# --- Configuração ---

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "language": "pt",
    "sample_rate": 16000,
    "channels": 1,
}


# --- Windows Hotkey API (RegisterHotKey) ---
# Substitui SetWindowsHookEx (usado pela lib keyboard) que morre silenciosamente.
# RegisterHotKey é message-based, não sofre com timeout, sobrevive a screen lock/UAC.

_user32 = ctypes.windll.user32

WM_HOTKEY = 0x0312
WM_QUIT = 0x0012

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_NOREPEAT = 0x4000

_VK_MAP = {
    "f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
    "f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
    "f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
    "space": 0x20, "enter": 0x0D, "tab": 0x09,
    "escape": 0x1B, "backspace": 0x08, "delete": 0x2E,
}

HOTKEY_ID = 1


def _parse_hotkey(hotkey_str: str) -> tuple[int, int]:
    """Converte string de hotkey em (modifiers, vk_code) para RegisterHotKey.

    Exemplos: "F9" → (MOD_NOREPEAT, 0x78)
              "ctrl+shift+space" → (MOD_CONTROL|MOD_SHIFT|MOD_NOREPEAT, 0x20)
    """
    modifiers = MOD_NOREPEAT
    vk = 0

    parts = [p.strip().lower() for p in hotkey_str.split("+")]
    for part in parts:
        if part in ("ctrl", "control"):
            modifiers |= MOD_CONTROL
        elif part in ("shift",):
            modifiers |= MOD_SHIFT
        elif part in ("alt",):
            modifiers |= MOD_ALT
        elif part in _VK_MAP:
            vk = _VK_MAP[part]
        elif len(part) == 1 and part.isalnum():
            vk = ord(part.upper())
        else:
            raise ValueError(f"Hotkey não reconhecida: '{part}' em '{hotkey_str}'")

    if vk == 0:
        raise ValueError(f"Nenhuma tecla principal encontrada em '{hotkey_str}'")

    return modifiers, vk


def _register_hotkey(hotkey_id: int, modifiers: int, vk: int) -> bool:
    """Registra hotkey global via Windows API. Retorna True se sucesso."""
    return bool(_user32.RegisterHotKey(None, hotkey_id, modifiers, vk))


def _unregister_hotkey(hotkey_id: int) -> None:
    """Remove registro de hotkey."""
    _user32.UnregisterHotKey(None, hotkey_id)


def _run_hotkey_loop(callback) -> None:
    """Message loop que processa WM_HOTKEY. Bloqueia a thread chamadora.

    Sai quando recebe WM_QUIT (via PostThreadMessage de outra thread).
    """
    msg = wintypes.MSG()
    while _user32.GetMessageA(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
            callback()
        _user32.TranslateMessage(ctypes.byref(msg))
        _user32.DispatchMessageA(ctypes.byref(msg))


# --- App ---


class DictationApp:
    def __init__(self, config: dict):
        self.config = config
        self._state = AppState.IDLE
        self._audio_frames: list = []
        self._audio_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self.stream = None
        self._main_thread_id = None

    def _set_state(self, state: AppState) -> None:
        """Atualiza estado e reflete no tray icon."""
        self._state = state
        _update_tray(state)

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

    def start(self):
        """Inicia o app de dictation."""
        _acquire_lock()
        _start_tray(on_quit_callback=self._quit)

        errors = self.preflight_checks()
        if errors:
            for e in errors:
                logger.error(f"  [PREFLIGHT] {e}")

        hotkey = self.config["hotkey"]
        logger.info("Whisper Dictation ativo.")
        logger.info(f"  Hotkey: {hotkey}")
        logger.info(f"  Idioma: {self.config['language']}")
        logger.info(f"  Log: {LOG_FILE}")
        logger.info(f"  Aperte {hotkey} para gravar. Aperte de novo para transcrever.")

        # RegisterHotKey — confiável, não morre silenciosamente como SetWindowsHookEx
        self._main_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        try:
            mods, vk = _parse_hotkey(hotkey)
        except ValueError as e:
            logger.error(f"  [ERRO] Hotkey inválida: {e}")
            return

        if not _register_hotkey(HOTKEY_ID, mods, vk):
            logger.error(f"  [ERRO] Falha ao registrar {hotkey} (em uso por outro app?)")
            return

        logger.info(f"  Hotkey registrada via RegisterHotKey (thread {self._main_thread_id})")

        try:
            _run_hotkey_loop(self.toggle_recording)
        except KeyboardInterrupt:
            pass
        finally:
            _unregister_hotkey(HOTKEY_ID)
            self._cleanup()
            _stop_tray()
            _release_lock()
            logger.info("Dictation encerrado.")

    def _quit(self):
        """Chamado pelo menu 'Sair' do tray."""
        logger.info("Saindo via tray menu...")
        if self._main_thread_id:
            # Posta WM_QUIT para o message loop do RegisterHotKey (main thread)
            # Isso faz GetMessageA retornar 0, saindo do loop naturalmente
            _user32.PostThreadMessageA(self._main_thread_id, WM_QUIT, 0, 0)
        else:
            os._exit(0)

    def toggle_recording(self):
        """Callback do hotkey — despacha trabalho para thread separada."""
        threading.Thread(target=self._handle_toggle, daemon=True).start()

    def _handle_toggle(self):
        """Processa o toggle em thread separada (fora do hook do Windows)."""
        with self._state_lock:
            if self._state in (AppState.IDLE, AppState.SUCCESS, AppState.ERROR):
                self._start_recording()
                return
            elif self._state == AppState.RECORDING:
                self._set_state(AppState.PROCESSING)
                self._stop_stream()
            else:
                # PROCESSING → ignora F9
                logger.info("  [!] Transcrevendo... aguarde.")
                return

        # Fora do lock — transcrição é lenta (chamada HTTP)
        self._transcribe_and_paste()

    def _start_recording(self):
        """Começa a gravar do microfone."""
        with self._audio_lock:
            self._audio_frames = []

        sample_rate = self.config["sample_rate"]
        channels = self.config["channels"]

        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"  [audio] {status}")
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
            logger.info("  [REC] Gravando... (aperte hotkey para parar)")
        except Exception as e:
            logger.error(f"  [ERRO] Falha ao abrir microfone: {e}")
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
        """Cola texto via clipboard com retry e verificação."""
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
        """Transcreve o áudio gravado e cola o texto."""
        temp_path = None
        try:
            audio_data = self._collect_audio()

            if audio_data is None:
                logger.info("  [!] Nenhum áudio capturado.")
                self._set_state(AppState.ERROR)
                return

            logger.info("  [...] Transcrevendo...")

            temp_path = (
                Path(tempfile.gettempdir()) / f"whisper_dictation_{os.getpid()}.wav"
            )
            wavfile.write(str(temp_path), self.config["sample_rate"], audio_data)

            text = self._transcribe_with_retry(str(temp_path))

            if text and text.strip():
                self._paste_text(text)
                logger.info(f'  [OK] "{text}"')
                self._set_state(AppState.SUCCESS)
                if _tray_available:
                    threading.Thread(
                        target=_flash_tray,
                        args=(AppState.SUCCESS, 2.0),
                        daemon=True,
                    ).start()
            else:
                logger.info("  [!] Transcrição vazia.")
                self._set_state(AppState.ERROR)

        except Exception as e:
            logger.error(f"  [ERRO] {e}")
            self._set_state(AppState.ERROR)

        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

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
