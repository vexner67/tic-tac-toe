import pytest

from tic_tac_toe.model import (
    WINDOW_SIZE_PRESETS,
    InvalidWindowSizeError,
    WindowSize,
)


def test_valid_size():
    size = WindowSize(500, 600)
    assert (size.width, size.height) == (500, 600)


def test_geometry_string():
    assert WindowSize(480, 560).as_geometry() == "480x560"


@pytest.mark.parametrize("width, height", [
    (WindowSize.MIN_WIDTH, WindowSize.MIN_HEIGHT),
    (WindowSize.MAX_WIDTH, WindowSize.MAX_HEIGHT),
])
def test_boundaries_are_inclusive(width, height):
    WindowSize(width, height)


@pytest.mark.parametrize("width, height", [
    (WindowSize.MIN_WIDTH - 1, 500),
    (WindowSize.MAX_WIDTH + 1, 500),
    (500, WindowSize.MIN_HEIGHT - 1),
    (500, WindowSize.MAX_HEIGHT + 1),
])
def test_out_of_range_size_raises(width, height):
    with pytest.raises(InvalidWindowSizeError):
        WindowSize(width, height)


def test_parse_strips_whitespace():
    assert WindowSize.parse(" 500 ", "600") == WindowSize(500, 600)


@pytest.mark.parametrize("width, height", [
    ("abc", "500"), ("500", ""), ("50.5", "500"),
])
def test_parse_non_integer_raises(width, height):
    with pytest.raises(InvalidWindowSizeError):
        WindowSize.parse(width, height)


def test_presets_are_valid_window_sizes():
    assert all(isinstance(s, WindowSize)
               for s in WINDOW_SIZE_PRESETS.values())
