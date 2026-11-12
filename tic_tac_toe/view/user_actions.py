"""Абстракция обработчиков действий пользователя, нужная представлению."""

from typing import Protocol

from tic_tac_toe.model import WindowSize


class UserActions(Protocol):
    """Действия, которые представление передаёт контроллеру."""

    @property
    def window_size(self) -> WindowSize:
        """Текущий размер окна."""

    def handle_cell_click(self, row: int, col: int) -> None:
        """Пользователь щёлкнул по клетке."""

    def handle_new_game(self) -> None:
        """Пользователь начал новую партию."""

    def handle_reset_score(self) -> None:
        """Пользователь сбросил счёт."""

    def handle_window_size(self, size: WindowSize) -> None:
        """Пользователь выбрал готовый размер окна."""

    def handle_custom_window_size(self, width: str, height: str) -> bool:
        """Пользователь ввёл размер окна вручную."""

    def handle_exit(self) -> None:
        """Пользователь закрывает приложение."""
