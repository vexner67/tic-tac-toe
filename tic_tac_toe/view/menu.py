"""Главное меню приложения."""

import tkinter as tk
from typing import Callable

from tic_tac_toe.model import WINDOW_SIZE_PRESETS
from tic_tac_toe.view.user_actions import UserActions

#: Значение переключателя размера, когда выбран нестандартный размер.
CUSTOM_SIZE = "custom"

RULES_TEXT = (
    "Игроки по очереди ставят свой знак (X или O) в свободную клетку "
    "поля 3×3.\n\n"
    "Побеждает тот, кто первым выстроит три своих знака в ряд — "
    "по горизонтали, вертикали или диагонали.\n\n"
    "Если все клетки заняты, а победителя нет, объявляется ничья.\n\n"
    "Право первого хода переходит от партии к партии."
)

ABOUT_TEXT = "Крестики-нолики для двух игроков.\nВерсия {version}."


class MainMenu(tk.Menu):
    """Меню «Игра», «Настройки» и «Справка»."""

    def __init__(
        self,
        root: tk.Tk,
        actions: UserActions,
        size_choice: tk.StringVar,
        open_size_dialog: Callable[[], None],
        show_info: Callable[[str, str], None],
        version: str,
    ) -> None:
        super().__init__(root)
        self._actions = actions
        self._size_choice = size_choice
        self.add_cascade(label="Игра", menu=self._game_menu())
        self.add_cascade(label="Настройки",
                         menu=self._settings_menu(open_size_dialog))
        self.add_cascade(label="Справка",
                         menu=self._help_menu(show_info, version))

    def _game_menu(self) -> tk.Menu:
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Новая партия", accelerator="Ctrl+N",
                         command=self._actions.handle_new_game)
        menu.add_command(label="Сбросить счёт",
                         command=self._actions.handle_reset_score)
        menu.add_separator()
        menu.add_command(label="Выход", accelerator="Ctrl+Q",
                         command=self._actions.handle_exit)
        return menu

    def _settings_menu(self, open_size_dialog: Callable[[], None]) -> tk.Menu:
        menu = tk.Menu(self, tearoff=False)
        sizes = tk.Menu(menu, tearoff=False)
        for label, size in WINDOW_SIZE_PRESETS.items():
            sizes.add_radiobutton(
                label=label, value=label, variable=self._size_choice,
                command=lambda s=size: self._actions.handle_window_size(s),
            )
        sizes.add_separator()
        sizes.add_radiobutton(label="Другой…", value=CUSTOM_SIZE,
                              variable=self._size_choice,
                              command=open_size_dialog)
        menu.add_cascade(label="Размер окна", menu=sizes)
        return menu

    def _help_menu(self, show_info: Callable[[str, str], None],
                   version: str) -> tk.Menu:
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label="Правила игры",
                         command=lambda: show_info("Правила игры",
                                                   RULES_TEXT))
        menu.add_command(
            label="О программе",
            command=lambda: show_info("О программе",
                                      ABOUT_TEXT.format(version=version)),
        )
        return menu
