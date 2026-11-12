from tic_tac_toe.model import Mark


def test_opponent_of_x_is_o():
    assert Mark.X.opponent is Mark.O


def test_opponent_of_o_is_x():
    assert Mark.O.opponent is Mark.X
