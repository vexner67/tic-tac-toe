import pytest

from tic_tac_toe.model import Mark, Match, Position
from tests.helpers import DRAW_SEQUENCE, X_WINS_TOP_ROW


@pytest.fixture
def match():
    return Match()


def play(match, moves):
    for position in moves:
        match.make_move(position)


def test_initial_score_is_zero(match):
    assert match.score.wins == {Mark.X: 0, Mark.O: 0}
    assert match.score.draws == 0
    assert match.first_mark is Mark.X


def test_win_is_recorded(match):
    play(match, X_WINS_TOP_ROW)
    assert match.score.wins[Mark.X] == 1


def test_draw_is_recorded(match):
    play(match, DRAW_SEQUENCE)
    assert match.score.draws == 1


def test_unfinished_game_is_not_recorded(match):
    match.make_move(Position(0, 0))
    assert match.score.wins == {Mark.X: 0, Mark.O: 0}
    assert match.score.draws == 0


def test_new_game_alternates_first_mark(match):
    match.new_game()
    assert match.first_mark is Mark.O
    assert match.game.current_mark is Mark.O
    match.new_game()
    assert match.game.current_mark is Mark.X


def test_new_game_keeps_score(match):
    play(match, X_WINS_TOP_ROW)
    match.new_game()
    assert match.score.wins[Mark.X] == 1
    assert not match.game.is_over


def test_reset_clears_score_and_game(match):
    play(match, X_WINS_TOP_ROW)
    match.new_game()
    match.reset()
    assert match.score.wins[Mark.X] == 0
    assert match.first_mark is Mark.X
    assert match.game.board.get(Position(0, 0)) is None
