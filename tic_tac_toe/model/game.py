"""Одна партия игры."""

from enum import Enum, auto
from typing import Optional

from tic_tac_toe.model.board import Board, Position
from tic_tac_toe.model.exceptions import GameOverError
from tic_tac_toe.model.mark import Mark
from tic_tac_toe.model.rules import Line, find_victory


class GameStatus(Enum):
    """Состояние партии."""

    IN_PROGRESS = auto()
    WON = auto()
    DRAW = auto()


class Game:
    """Партия: очередность ходов и определение исхода."""

    def __init__(self, first_mark: Mark = Mark.X) -> None:
        self.board = Board()
        self.current_mark = first_mark
        self.status = GameStatus.IN_PROGRESS
        self.winner: Optional[Mark] = None
        self.winning_line: Line = ()

    @property
    def is_over(self) -> bool:
        """Завершена ли партия."""
        return self.status is not GameStatus.IN_PROGRESS

    def make_move(self, position: Position) -> None:
        """Сделать ход текущим игроком и передать ход сопернику.

        :raises GameOverError: партия уже завершена.
        :raises InvalidPositionError: клетка вне поля.
        :raises CellOccupiedError: клетка занята.
        """
        if self.is_over:
            raise GameOverError()
        self.board.place(position, self.current_mark)
        self._update_status()
        if not self.is_over:
            self.current_mark = self.current_mark.opponent

    def _update_status(self) -> None:
        """Пересчитать состояние партии после хода."""
        victory = find_victory(self.board)
        if victory is not None:
            self.status = GameStatus.WON
            self.winner = victory.mark
            self.winning_line = victory.line
        elif self.board.is_full():
            self.status = GameStatus.DRAW
