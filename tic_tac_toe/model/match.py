"""Серия партий между двумя игроками и общий счёт."""

from dataclasses import dataclass, field

from tic_tac_toe.model.board import Position
from tic_tac_toe.model.game import Game, GameStatus
from tic_tac_toe.model.mark import Mark


@dataclass
class Score:
    """Счёт серии: число побед каждого знака и ничьих."""

    wins: dict[Mark, int] = field(
        default_factory=lambda: {mark: 0 for mark in Mark}
    )
    draws: int = 0

    def record(self, game: Game) -> None:
        """Учесть результат завершённой партии."""
        if game.status is GameStatus.WON and game.winner is not None:
            self.wins[game.winner] += 1
        elif game.status is GameStatus.DRAW:
            self.draws += 1


class Match:
    """Серия партий.

    Право первого хода чередуется между партиями, чтобы игроки были
    в равных условиях. Результат каждой партии автоматически заносится
    в счёт.
    """

    def __init__(self) -> None:
        self.score = Score()
        self._first_mark = Mark.X
        self.game = Game(self._first_mark)

    @property
    def first_mark(self) -> Mark:
        """Знак игрока, начавшего текущую партию."""
        return self._first_mark

    def make_move(self, position: Position) -> None:
        """Сделать ход в текущей партии и обновить счёт при её окончании."""
        self.game.make_move(position)
        if self.game.is_over:
            self.score.record(self.game)

    def new_game(self) -> None:
        """Начать новую партию; первым ходит соперник прошлого начинающего."""
        self._first_mark = self._first_mark.opponent
        self.game = Game(self._first_mark)

    def reset(self) -> None:
        """Обнулить счёт и начать серию заново."""
        self.score = Score()
        self._first_mark = Mark.X
        self.game = Game(self._first_mark)
