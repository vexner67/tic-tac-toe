import pytest

from tic_tac_toe.model import (
    BOARD_SIZE,
    Board,
    CellOccupiedError,
    InvalidPositionError,
    Mark,
    Position,
)


@pytest.fixture
def board():
    return Board()


def test_new_board_is_empty(board):
    assert all(board.get(p) is None for p in board.positions())


def test_positions_cover_whole_board(board):
    assert len(list(board.positions())) == BOARD_SIZE ** 2


def test_place_puts_mark(board):
    board.place(Position(1, 2), Mark.O)
    assert board.get(Position(1, 2)) is Mark.O


def test_place_into_occupied_cell_raises(board):
    board.place(Position(0, 0), Mark.X)
    with pytest.raises(CellOccupiedError):
        board.place(Position(0, 0), Mark.O)
    assert board.get(Position(0, 0)) is Mark.X


@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (3, 0), (0, 3)])
def test_out_of_bounds_position_raises(board, row, col):
    with pytest.raises(InvalidPositionError):
        board.place(Position(row, col), Mark.X)


def test_is_full(board):
    for index, position in enumerate(board.positions()):
        assert not board.is_full()
        board.place(position, Mark.X if index % 2 else Mark.O)
    assert board.is_full()
