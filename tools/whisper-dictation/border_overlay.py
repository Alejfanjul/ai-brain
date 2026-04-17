"""
Border Overlay — indicador visual de borda na tela inteira.

Pensado para acessibilidade (ex: Stargardt, baixa visão central).
A borda colorida é percebida pela visão periférica, que costuma estar preservada.

Quatro janelas finas topmost (top/bottom/left/right) com click-through via
WS_EX_TRANSPARENT, para não bloquear interação do usuário.

Uso:
    overlay = BorderOverlay(thickness=12, enabled=True)
    overlay.show("#FF0000")
    overlay.hide()
    overlay.set_enabled(False)
    overlay.stop()
"""

import ctypes
import logging
import threading

logger = logging.getLogger("dictation")


_GWL_EXSTYLE = -20
_WS_EX_LAYERED = 0x00080000
_WS_EX_TRANSPARENT = 0x00000020
_WS_EX_TOOLWINDOW = 0x00000080
_WS_EX_NOACTIVATE = 0x08000000
_LWA_ALPHA = 0x00000002


class BorderOverlay:
    """Borda colorida topmost ao redor da tela, com click-through."""

    def __init__(self, thickness: int = 12, enabled: bool = True):
        self.thickness = thickness
        self.enabled = enabled
        self._root = None
        self._windows: list = []
        self._ready = threading.Event()
        self._started = False
        self._start()

    def _start(self) -> None:
        """Inicia thread tkinter dedicada."""
        if self._started:
            return
        self._started = True
        threading.Thread(target=self._run, daemon=True).start()
        if not self._ready.wait(timeout=3):
            logger.warning("  [border] Timeout ao iniciar overlay de borda.")

    def _run(self) -> None:
        try:
            import tkinter as tk

            self._root = tk.Tk()
            self._root.withdraw()
            self._create_border_windows(tk)
            self._ready.set()
            self._root.mainloop()
        except Exception as e:
            logger.error(f"  [border] Falha ao iniciar overlay: {e}")
            self._ready.set()

    def _create_border_windows(self, tk) -> None:
        screen_w = self._root.winfo_screenwidth()
        screen_h = self._root.winfo_screenheight()
        t = self.thickness

        positions = [
            (screen_w, t, 0, 0),                   # top
            (screen_w, t, 0, screen_h - t),        # bottom
            (t, screen_h, 0, 0),                   # left
            (t, screen_h, screen_w - t, 0),        # right
        ]

        for w, h, x, y in positions:
            win = tk.Toplevel(self._root)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            win.geometry(f"{w}x{h}+{x}+{y}")
            win.configure(bg="#808080")
            win.withdraw()
            self._make_click_through(win)
            self._windows.append(win)

    def _make_click_through(self, win) -> None:
        """Aplica WS_EX_TRANSPARENT + WS_EX_LAYERED: cliques atravessam a janela.

        Após ligar WS_EX_LAYERED é obrigatório chamar SetLayeredWindowAttributes,
        caso contrário a janela não renderiza nada (fica invisível).
        """
        try:
            win.update_idletasks()
            hwnd = win.winfo_id()
            user32 = ctypes.windll.user32
            ex_style = user32.GetWindowLongW(hwnd, _GWL_EXSTYLE)
            user32.SetWindowLongW(
                hwnd,
                _GWL_EXSTYLE,
                ex_style
                | _WS_EX_LAYERED
                | _WS_EX_TRANSPARENT
                | _WS_EX_TOOLWINDOW
                | _WS_EX_NOACTIVATE,
            )
            # Opacidade 100% — sem isso a janela layered não aparece
            user32.SetLayeredWindowAttributes(hwnd, 0, 255, _LWA_ALPHA)
        except Exception as e:
            logger.warning(f"  [border] Falha ao aplicar click-through: {e}")

    def show(self, color: str) -> None:
        """Mostra borda com a cor dada. Se desabilitada ou sem root, no-op."""
        if not self.enabled or self._root is None or not self._windows:
            return

        def _do():
            for w in self._windows:
                try:
                    w.configure(bg=color)
                    w.deiconify()
                    w.attributes("-topmost", True)
                except Exception:
                    pass

        try:
            self._root.after(0, _do)
        except Exception:
            pass

    def hide(self) -> None:
        """Esconde a borda."""
        if self._root is None or not self._windows:
            return

        def _do():
            for w in self._windows:
                try:
                    w.withdraw()
                except Exception:
                    pass

        try:
            self._root.after(0, _do)
        except Exception:
            pass

    def set_enabled(self, enabled: bool) -> None:
        """Liga/desliga a borda. Se desliga, esconde imediatamente."""
        self.enabled = enabled
        if not enabled:
            self.hide()

    def stop(self) -> None:
        """Encerra a thread tkinter."""
        if self._root is None:
            return
        try:
            self._root.after(0, self._root.quit)
        except Exception:
            pass
