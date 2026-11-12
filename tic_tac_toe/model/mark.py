"""Знаки игроков."""

from enum import Enum


class Mark(Enum):
    """Знак, которым ходит игрок: крестик или нолик."""

    X = "X"
    O = "O"  # noqa: E741 — буква «O» является частью предметной области

    @property
    def opponent(self) -> "Mark":
        """Знак соперника."""
        return Mark.O if self is Mark.X else Mark.X
