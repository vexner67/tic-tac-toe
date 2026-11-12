"""Модель предметной области: поле, ходы, правила, партии и счёт."""

from tic_tac_toe.model.board import BOARD_SIZE, Board, Position
from tic_tac_toe.model.exceptions import (
    CellOccupiedError,
    GameOverError,
    InvalidPositionError,
    InvalidWindowSizeError,
    TicTacToeError,
)
from tic_tac_toe.model.game import Game, GameStatus
from tic_tac_toe.model.mark import Mark
from tic_tac_toe.model.match import Match, Score
from tic_tac_toe.model.window_size import WINDOW_SIZE_PRESETS, WindowSize

__all__ = [
    "BOARD_SIZE",
    "Board",
    "CellOccupiedError",
    "Game",
    "GameOverError",
    "GameStatus",
    "InvalidPositionError",
    "InvalidWindowSizeError",
    "Mark",
    "Match",
    "Position",
    "Score",
    "TicTacToeError",
    "WINDOW_SIZE_PRESETS",
    "WindowSize",
]
