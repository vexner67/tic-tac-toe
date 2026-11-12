"""Игровое поле."""

from dataclasses import dataclass
from typing import Iterator, Optional

from tic_tac_toe.model.exceptions import (
    CellOccupiedError,
    InvalidPositionError,
)
from tic_tac_toe.model.mark import Mark

#: Размер стороны квадратного поля (классическое поле 3×3).
BOARD_SIZE = 3


@dataclass(frozen=True)
class Position:
    """Координаты клетки поля (нумерация с нуля)."""

    row: int
    col: int


class Board:
    """Квадратное поле ``BOARD_SIZE × BOARD_SIZE``.

    Отвечает только за хранение знаков и корректность их размещения;
    правила определения победителя вынесены в модуль ``rules``.
    """

    size = BOARD_SIZE

    def __init__(self) -> None:
        self._cells: list[list[Optional[Mark]]] = [
            [None] * self.size for _ in range(self.size)
        ]

    def get(self, position: Position) -> Optional[Mark]:
        """Вернуть знак в клетке или ``None``, если клетка пуста."""
        self._validate(position)
        return self._cells[position.row][position.col]

    def place(self, position: Position, mark: Mark) -> None:
        """Поставить знак в пустую клетку.

        :raises InvalidPositionError: клетка вне поля.
        :raises CellOccupiedError: клетка уже занята.
        """
        if self.get(position) is not None:
            raise CellOccupiedError(position.row, position.col)
        self._cells[position.row][position.col] = mark

    def is_full(self) -> bool:
        """Заполнены ли все клетки поля."""
        return all(mark is not None for row in self._cells for mark in row)

    def positions(self) -> Iterator[Position]:
        """Перебрать все клетки поля построчно."""
        for row in range(self.size):
            for col in range(self.size):
                yield Position(row, col)

    def _validate(self, position: Position) -> None:
        """Убедиться, что координаты лежат в пределах поля."""
        if not (0 <= position.row < self.size
                and 0 <= position.col < self.size):
            raise InvalidPositionError(position.row, position.col)
