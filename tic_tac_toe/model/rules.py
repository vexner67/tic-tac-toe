"""Правила определения победителя."""

from dataclasses import dataclass
from typing import Optional

from tic_tac_toe.model.board import BOARD_SIZE, Board, Position
from tic_tac_toe.model.mark import Mark

Line = tuple[Position, ...]


def _build_win_lines(size: int) -> tuple[Line, ...]:
    """Построить все выигрышные линии: строки, столбцы и две диагонали."""
    indices = range(size)
    rows = [tuple(Position(r, c) for c in indices) for r in indices]
    cols = [tuple(Position(r, c) for r in indices) for c in indices]
    main_diagonal = tuple(Position(i, i) for i in indices)
    anti_diagonal = tuple(Position(i, size - 1 - i) for i in indices)
    return tuple(rows + cols + [main_diagonal, anti_diagonal])


#: Все линии, заполнение которых одним знаком означает победу.
WIN_LINES: tuple[Line, ...] = _build_win_lines(BOARD_SIZE)


@dataclass(frozen=True)
class Victory:
    """Результат победы: знак победителя и выигрышная линия."""

    mark: Mark
    line: Line


def find_victory(board: Board) -> Optional[Victory]:
    """Найти победителя на поле или вернуть ``None``."""
    for line in WIN_LINES:
        first = board.get(line[0])
        if first is not None and all(board.get(p) is first for p in line):
            return Victory(first, line)
    return None
