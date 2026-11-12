"""Абстракция представления, от которой зависит контроллер (DIP)."""

from typing import Protocol

from tic_tac_toe.controller.view_state import ViewState
from tic_tac_toe.model import WindowSize


class GameView(Protocol):
    """Операции, которые контроллер может запросить у представления."""

    def render(self, state: ViewState) -> None:
        """Отобразить актуальное состояние игры."""

    def show_message(self, title: str, text: str) -> None:
        """Показать информационное сообщение."""

    def show_error(self, text: str) -> None:
        """Показать сообщение об ошибке."""

    def apply_window_size(self, size: WindowSize) -> None:
        """Изменить размер главного окна."""

    def close(self) -> None:
        """Закрыть приложение."""
