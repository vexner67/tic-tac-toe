import pytest

from tic_tac_toe.model import Board, Mark
from tic_tac_toe.model.rules import WIN_LINES, find_victory


def test_there_are_eight_win_lines():
    assert len(WIN_LINES) == 8


def test_empty_board_has_no_victory():
    assert find_victory(Board()) is None


@pytest.mark.parametrize("line", WIN_LINES)
def test_any_full_line_wins(line):
    board = Board()
    for position in line:
        board.place(position, Mark.O)
    victory = find_victory(board)
    assert victory is not None
    assert victory.mark is Mark.O
    assert victory.line == line


def test_mixed_line_does_not_win():
    board = Board()
    first, second, third = WIN_LINES[0]
    board.place(first, Mark.X)
    board.place(second, Mark.O)
    board.place(third, Mark.X)
    assert find_victory(board) is None
