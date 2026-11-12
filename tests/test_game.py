import pytest

from tic_tac_toe.model import (
    CellOccupiedError,
    Game,
    GameOverError,
    GameStatus,
    Mark,
    Position,
)
from tests.helpers import DRAW_SEQUENCE, X_WINS_TOP_ROW, positions


def play(game, moves):
    for position in moves:
        game.make_move(position)


def test_new_game_state():
    game = Game()
    assert game.status is GameStatus.IN_PROGRESS
    assert game.current_mark is Mark.X
    assert game.winner is None
    assert game.winning_line == ()
    assert not game.is_over


def test_first_mark_can_be_chosen():
    assert Game(Mark.O).current_mark is Mark.O


def test_turns_alternate():
    game = Game()
    game.make_move(Position(0, 0))
    assert game.current_mark is Mark.O
    game.make_move(Position(1, 1))
    assert game.current_mark is Mark.X


def test_failed_move_keeps_turn():
    game = Game()
    game.make_move(Position(0, 0))
    with pytest.raises(CellOccupiedError):
        game.make_move(Position(0, 0))
    assert game.current_mark is Mark.O


def test_win_is_detected():
    game = Game()
    play(game, X_WINS_TOP_ROW)
    assert game.status is GameStatus.WON
    assert game.winner is Mark.X
    assert game.current_mark is Mark.X
    assert game.winning_line == tuple(positions((0, 0), (0, 1), (0, 2)))


def test_draw_is_detected():
    game = Game()
    play(game, DRAW_SEQUENCE)
    assert game.status is GameStatus.DRAW
    assert game.winner is None


def test_win_on_last_move_is_not_draw():
    #  X | O | X
    #  O | X | O
    #  O | X | X   <- последний ход X в (2, 2) даёт победу по диагонали
    game = Game()
    play(game, positions(
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 1),
        (1, 2), (2, 1), (2, 0), (2, 2),
    ))
    assert game.status is GameStatus.WON
    assert game.winner is Mark.X


def test_move_after_game_over_raises():
    game = Game()
    play(game, X_WINS_TOP_ROW)
    with pytest.raises(GameOverError):
        game.make_move(Position(2, 2))
