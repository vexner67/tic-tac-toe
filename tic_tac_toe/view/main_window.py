"""Главное окно приложения — реализация ``GameView`` на tkinter."""

import logging
import tkinter as tk
from tkinter import messagebox
from types import TracebackType
from typing import Optional

from tic_tac_toe import __version__
from tic_tac_toe.controller import ViewState
from tic_tac_toe.model import WINDOW_SIZE_PRESETS, WindowSize
from tic_tac_toe.view import theme
from tic_tac_toe.view.board_canvas import BoardCanvas
from tic_tac_toe.view.menu import CUSTOM_SIZE, MainMenu
from tic_tac_toe.view.size_dialog import WindowSizeDialog
from tic_tac_toe.view.user_actions import UserActions

logger = logging.getLogger(__name__)

TITLE = "Крестики-нолики"


class MainWindow:
    """Окно с меню, строкой состояния, полем и табло счёта."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title(TITLE)
        self._root.configure(background=theme.BACKGROUND)
        self._root.minsize(WindowSize.MIN_WIDTH, WindowSize.MIN_HEIGHT)
        self._root.maxsize(WindowSize.MAX_WIDTH, WindowSize.MAX_HEIGHT)
        # Любое непредвиденное исключение в обработчике событий tkinter
        # попадает сюда: оно логируется и показывается пользователю,
        # а приложение продолжает работу.
        self._root.report_callback_exception = self._on_unexpected_error
        self._size_choice = tk.StringVar()
        self._actions: Optional[UserActions] = None
        self._status = self._label(theme.STATUS_FONT)
        self._board: Optional[BoardCanvas] = None
        self._score = self._label(theme.SCORE_FONT)

    def attach(self, actions: UserActions) -> None:
        """Подключить обработчики действий и построить интерфейс."""
        self._actions = actions
        self._root.config(menu=MainMenu(
            self._root, actions, self._size_choice,
            open_size_dialog=self._open_size_dialog,
            show_info=self.show_message,
            version=__version__,
        ))
        # Табло упаковывается раньше поля, чтобы при уменьшении окна
        # растягиваемый холст не вытеснил его за границу.
        self._status.pack(side=tk.TOP, pady=(10, 0))
        self._score.pack(side=tk.BOTTOM, pady=(0, 10))
        self._board = BoardCanvas(self._root, actions.handle_cell_click)
        self._board.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._root.bind("<Control-n>", lambda _e: actions.handle_new_game())
        self._root.bind("<Control-q>", lambda _e: actions.handle_exit())
        self._root.protocol("WM_DELETE_WINDOW", actions.handle_exit)

    def run(self) -> None:
        """Запустить цикл обработки событий."""
        self._root.mainloop()

    # --- реализация GameView ---------------------------------------------

    def render(self, state: ViewState) -> None:
        self._status.configure(text=state.status)
        self._score.configure(text=state.score)
        if self._board is not None:
            self._board.show(state)

    def show_message(self, title: str, text: str) -> None:
        messagebox.showinfo(title, text, parent=self._root)

    def show_error(self, text: str) -> None:
        messagebox.showwarning("Ошибка", text, parent=self._root)

    def apply_window_size(self, size: WindowSize) -> None:
        self._root.geometry(size.as_geometry())
        self._size_choice.set(_preset_label(size))

    def close(self) -> None:
        self._root.destroy()

    # --- вспомогательные методы ------------------------------------------

    def _label(self, font: tuple) -> tk.Label:
        return tk.Label(self._root, font=font, foreground=theme.TEXT,
                        background=theme.BACKGROUND)

    def _open_size_dialog(self) -> None:
        if self._actions is None:
            return
        # До подтверждения в меню остаётся отмеченным текущий размер.
        self._size_choice.set(_preset_label(self._actions.window_size))
        WindowSizeDialog(self._root, self._actions.window_size,
                         self._actions.handle_custom_window_size)

    def _on_unexpected_error(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: Optional[TracebackType],
    ) -> None:
        logger.error("Непредвиденная ошибка",
                     exc_info=(exc_type, exc_value, exc_tb))
        messagebox.showerror(
            "Непредвиденная ошибка",
            f"Произошла ошибка: {exc_value}\n"
            "Приложение продолжит работу.",
            parent=self._root,
        )


def _preset_label(size: WindowSize) -> str:
    """Название готового размера или ``CUSTOM_SIZE`` для нестандартного."""
    for label, preset in WINDOW_SIZE_PRESETS.items():
        if preset == size:
            return label
    return CUSTOM_SIZE
