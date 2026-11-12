import pytest

from tic_tac_toe.controller import GameController
from tic_tac_toe.controller.game_controller import RESULT_TITLE
from tic_tac_toe.model import (
    DEFAULT_WINDOW_SIZE,
    Match,
    Position,
    WindowSize,
)
from tests.helpers import DRAW_SEQUENCE, X_WINS_TOP_ROW


class FakeView:
    """Тестовый двойник представления, запоминающий все вызовы."""

    def __init__(self):
        self.states = []
        self.messages = []
        self.errors = []
        self.sizes = []
        self.closed = False

    @property
    def state(self):
        return self.states[-1]

    def render(self, state):
        self.states.append(state)

    def show_message(self, title, text):
        self.messages.append((title, text))

    def show_error(self, text):
        self.errors.append(text)

    def apply_window_size(self, size):
        self.sizes.append(size)

    def close(self):
        self.closed = True


@pytest.fixture
def view():
    return FakeView()


@pytest.fixture
def controller(view):
    controller = GameController(Match(), view)
    controller.start()
    return controller


def click_all(controller, moves):
    for position in moves:
        controller.handle_cell_click(position.row, position.col)


def test_start_renders_empty_board_and_sets_size(controller, view):
    assert view.sizes == [DEFAULT_WINDOW_SIZE]
    assert view.state.cells == (("", "", ""),) * 3
    assert view.state.status == "Ходят X"
    assert view.state.score == "X: 0    O: 0    Ничьи: 0"
    assert not view.state.locked
    assert view.state.highlighted == frozenset()


def test_click_places_mark_and_passes_turn(controller, view):
    controller.handle_cell_click(1, 1)
    assert view.state.cells[1][1] == "X"
    assert view.state.status == "Ходят O"


def test_click_on_occupied_cell_shows_error(controller, view):
    controller.handle_cell_click(0, 0)
    rendered = len(view.states)
    controller.handle_cell_click(0, 0)
    assert view.errors == ["Клетка (1, 1) уже занята."]
    assert len(view.states) == rendered


def test_click_outside_board_shows_error(controller, view):
    controller.handle_cell_click(5, 5)
    assert len(view.errors) == 1


def test_win_locks_board_and_reports_result(controller, view):
    click_all(controller, X_WINS_TOP_ROW)
    assert view.state.locked
    assert view.state.status == "Победили X!"
    assert view.state.highlighted == frozenset(
        {Position(0, 0), Position(0, 1), Position(0, 2)}
    )
    assert view.state.score.startswith("X: 1")
    assert view.messages == [(RESULT_TITLE, "Победили X!")]


def test_draw_is_reported(controller, view):
    click_all(controller, DRAW_SEQUENCE)
    assert view.state.status == "Ничья!"
    assert view.state.score.endswith("Ничьи: 1")


def test_click_after_game_over_shows_error(controller, view):
    click_all(controller, X_WINS_TOP_ROW)
    controller.handle_cell_click(2, 2)
    assert view.errors == ["Партия окончена. Начните новую игру."]


def test_new_game_clears_board_and_keeps_score(controller, view):
    click_all(controller, X_WINS_TOP_ROW)
    controller.handle_new_game()
    assert view.state.cells == (("", "", ""),) * 3
    assert view.state.status == "Ходят O"
    assert view.state.score.startswith("X: 1")


def test_reset_score(controller, view):
    click_all(controller, X_WINS_TOP_ROW)
    controller.handle_reset_score()
    assert view.state.score == "X: 0    O: 0    Ничьи: 0"
    assert view.state.status == "Ходят X"


def test_window_size_preset_is_applied(controller, view):
    size = WindowSize(640, 740)
    controller.handle_window_size(size)
    assert view.sizes[-1] == size
    assert controller.window_size == size


def test_valid_custom_window_size_is_applied(controller, view):
    assert controller.handle_custom_window_size("500", "600")
    assert view.sizes[-1] == WindowSize(500, 600)


@pytest.mark.parametrize("width, height", [("abc", "600"), ("10", "600")])
def test_invalid_custom_window_size_shows_error(
        controller, view, width, height):
    assert not controller.handle_custom_window_size(width, height)
    assert len(view.errors) == 1
    assert controller.window_size == DEFAULT_WINDOW_SIZE


def test_exit_closes_view(controller, view):
    controller.handle_exit()
    assert view.closed
