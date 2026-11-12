"""Контроллер игры."""

from typing import Optional

from tic_tac_toe.controller.view_protocol import GameView
from tic_tac_toe.controller.view_state import ViewState
from tic_tac_toe.model import (
    DEFAULT_WINDOW_SIZE,
    Game,
    GameStatus,
    Mark,
    Match,
    Position,
    TicTacToeError,
    WindowSize,
)

RESULT_TITLE = "Итог партии"


def _symbol(mark: Optional[Mark]) -> str:
    """Символ для отображения знака; пустая строка для пустой клетки."""
    return mark.value if mark is not None else ""


class GameController:
    """Обрабатывает действия пользователя.

    Каждый обработчик перехватывает ожидаемые ошибки модели
    (``TicTacToeError``) и сообщает о них через представление, поэтому
    некорректное действие пользователя никогда не завершает программу.
    """

    def __init__(
        self,
        match: Match,
        view: GameView,
        window_size: WindowSize = DEFAULT_WINDOW_SIZE,
    ) -> None:
        self._match = match
        self._view = view
        self._window_size = window_size

    @property
    def window_size(self) -> WindowSize:
        """Текущий размер окна."""
        return self._window_size

    def start(self) -> None:
        """Подготовить представление к первой партии."""
        self._view.apply_window_size(self._window_size)
        self._refresh()

    def handle_cell_click(self, row: int, col: int) -> None:
        """Сделать ход в клетку ``(row, col)``."""
        try:
            self._match.make_move(Position(row, col))
        except TicTacToeError as error:
            self._view.show_error(str(error))
            return
        self._refresh()
        if self._match.game.is_over:
            self._view.show_message(RESULT_TITLE, self._status_text())

    def handle_new_game(self) -> None:
        """Начать новую партию с сохранением счёта."""
        self._match.new_game()
        self._refresh()

    def handle_reset_score(self) -> None:
        """Обнулить счёт и начать серию заново."""
        self._match.reset()
        self._refresh()

    def handle_window_size(self, size: WindowSize) -> None:
        """Применить выбранный размер окна."""
        self._window_size = size
        self._view.apply_window_size(size)

    def handle_custom_window_size(self, width: str, height: str) -> bool:
        """Применить размер окна, введённый пользователем вручную.

        :returns: ``True``, если размер корректен и применён.
        """
        try:
            size = WindowSize.parse(width, height)
        except TicTacToeError as error:
            self._view.show_error(str(error))
            return False
        self.handle_window_size(size)
        return True

    def handle_exit(self) -> None:
        """Завершить работу приложения."""
        self._view.close()

    def _refresh(self) -> None:
        """Передать представлению актуальное состояние."""
        self._view.render(self._build_state())

    def _build_state(self) -> ViewState:
        """Сформировать снимок состояния для представления."""
        game = self._match.game
        return ViewState(
            cells=self._cells(game),
            highlighted=frozenset(game.winning_line),
            locked=game.is_over,
            status=self._status_text(),
            score=self._score_text(),
        )

    @staticmethod
    def _cells(game: Game) -> tuple[tuple[str, ...], ...]:
        """Перевести поле в строки для отображения."""
        board = game.board
        indices = range(board.size)
        return tuple(
            tuple(_symbol(board.get(Position(r, c))) for c in indices)
            for r in indices
        )

    def _status_text(self) -> str:
        """Текст строки состояния."""
        game = self._match.game
        if game.status is GameStatus.WON and game.winner is not None:
            return f"Победили {game.winner.value}!"
        if game.status is GameStatus.DRAW:
            return "Ничья!"
        return f"Ходят {game.current_mark.value}"

    def _score_text(self) -> str:
        """Текст табло со счётом."""
        score = self._match.score
        parts = [f"{mark.value}: {wins}" for mark, wins in score.wins.items()]
        parts.append(f"Ничьи: {score.draws}")
        return "    ".join(parts)
