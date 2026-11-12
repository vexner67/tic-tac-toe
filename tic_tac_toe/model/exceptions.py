"""Исключения предметной области.

Все ожидаемые ошибки наследуются от ``TicTacToeError``, поэтому
контроллер может перехватывать их единообразно и показывать пользователю
понятное сообщение, не завершая программу.
"""


class TicTacToeError(Exception):
    """Базовое исключение приложения."""


class InvalidPositionError(TicTacToeError):
    """Координаты клетки выходят за пределы поля."""

    def __init__(self, row: int, col: int) -> None:
        super().__init__(f"Клетка ({row}, {col}) находится вне поля.")
        self.row = row
        self.col = col


class CellOccupiedError(TicTacToeError):
    """Попытка поставить знак в уже занятую клетку."""

    def __init__(self, row: int, col: int) -> None:
        super().__init__(f"Клетка ({row + 1}, {col + 1}) уже занята.")
        self.row = row
        self.col = col


class GameOverError(TicTacToeError):
    """Попытка сделать ход после окончания партии."""

    def __init__(self) -> None:
        super().__init__("Партия окончена. Начните новую игру.")


class InvalidWindowSizeError(TicTacToeError):
    """Некорректный размер окна, заданный пользователем."""
