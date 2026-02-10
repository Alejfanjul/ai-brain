"""
System tray icon para Whisper Dictation.

Mostra estado visual ao lado do relógio do Windows:
  - Cinza:    idle (esperando F9)
  - Vermelho: gravando
  - Amarelo:  transcrevendo
  - Verde:    sucesso (flash ~2s)
  - Vermelho claro: erro (flash ~2s)
"""

import pystray
from PIL import Image, ImageDraw

from dictation import AppState

# Cores por estado
STATE_COLORS = {
    AppState.IDLE: "#808080",
    AppState.RECORDING: "#FF0000",
    AppState.PROCESSING: "#FFD700",
    AppState.SUCCESS: "#00CC00",
    AppState.ERROR: "#FF4444",
}

STATE_TOOLTIPS = {
    AppState.IDLE: "Whisper Dictation — Pronto (F9)",
    AppState.RECORDING: "Gravando... (F9 para parar)",
    AppState.PROCESSING: "Transcrevendo...",
    AppState.SUCCESS: "Transcrito com sucesso!",
    AppState.ERROR: "Erro na transcrição",
}


def create_icon_image(color: str, size: int = 64) -> Image.Image:
    """Cria ícone circular com a cor especificada."""
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    margin = 4
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=color,
        outline="#333333",
        width=2,
    )
    return image


class TrayManager:
    def __init__(self):
        self._icon = None
        self._icons_cache = {}
        self._build_icons_cache()

    def _build_icons_cache(self):
        for state, color in STATE_COLORS.items():
            self._icons_cache[state] = create_icon_image(color)

    def update_state(self, state: AppState):
        """Atualiza ícone e tooltip. Thread-safe (pystray usa message pump)."""
        if self._icon:
            self._icon.icon = self._icons_cache[state]
            self._icon.title = STATE_TOOLTIPS[state]

    def _create_menu(self, config: dict):
        hotkey = config.get("hotkey", "F9")
        language = config.get("language", "pt")
        return pystray.Menu(
            pystray.MenuItem(
                "Whisper Dictation",
                None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(f"Hotkey: {hotkey}", None, enabled=False),
            pystray.MenuItem(f"Idioma: {language}", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Sair", self._quit),
        )

    def _quit(self, icon, item):
        icon.stop()

    def run(self, setup_callback, config: dict):
        """Inicia o tray icon. Bloqueia na thread atual (message pump do Windows)."""
        self._icon = pystray.Icon(
            name="whisper-dictation",
            icon=self._icons_cache[AppState.IDLE],
            title=STATE_TOOLTIPS[AppState.IDLE],
            menu=self._create_menu(config),
        )
        self._icon.run(setup=setup_callback)
