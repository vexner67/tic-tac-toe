import pytest

from tic_tac_toe.view.geometry import BoardGeometry


@pytest.fixture
def geometry():
    # Холст 320×320, отступ 10 → поле 300×300, клетка 100×100.
    return BoardGeometry(width=320, height=320, size=3, margin=10)


def test_side_and_cell(geometry):
    assert geometry.side == 300
    assert geometry.cell == 100


def test_board_is_centered_on_wide_canvas():
    geometry = BoardGeometry(width=520, height=320, size=3, margin=10)
    assert geometry.origin == (110, 10)


@pytest.mark.parametrize("x, y, expected", [
    (15, 15, (0, 0)),
    (305, 15, (0, 2)),
    (160, 160, (1, 1)),
    (15, 305, (2, 0)),
])
def test_cell_at_inside(geometry, x, y, expected):
    assert geometry.cell_at(x, y) == expected


@pytest.mark.parametrize("x, y", [(5, 5), (315, 160), (160, 315)])
def test_cell_at_outside_returns_none(geometry, x, y):
    assert geometry.cell_at(x, y) is None


def test_cell_at_on_degenerate_canvas_returns_none():
    assert BoardGeometry(10, 10, 3).cell_at(5, 5) is None


def test_cell_rect(geometry):
    assert geometry.cell_rect(1, 2) == (210, 110, 310, 210)
