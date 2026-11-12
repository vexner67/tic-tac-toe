"""Вспомогательные функции для тестов."""

from tic_tac_toe.model import Position


def positions(*coords: tuple[int, int]) -> list[Position]:
    """Преобразовать пары координат в список ``Position``."""
    return [Position(row, col) for row, col in coords]


#: Последовательность ходов, в которой X побеждает по верхней строке.
X_WINS_TOP_ROW = positions((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))

#: Последовательность ходов, заканчивающаяся ничьей.
#:  X | O | X
#:  X | O | O
#:  O | X | X
DRAW_SEQUENCE = positions(
    (0, 0), (0, 1), (0, 2), (1, 1), (1, 0),
    (1, 2), (2, 1), (2, 0), (2, 2),
)
