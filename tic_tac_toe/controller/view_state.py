"""Неизменяемый «снимок» того, что должно быть показано пользователю.

Представление получает только эти данные и не зависит от классов модели
напрямую, что упрощает его замену и тестирование контроллера.
"""

from dataclasses import dataclass

from tic_tac_toe.model import Position

#: Строки поля: ``"X"``, ``"O"`` или ``""`` для пустой клетки.
Cells = tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class ViewState:
    """Состояние экрана игры."""

    cells: Cells
    highlighted: frozenset[Position]
    locked: bool
    status: str
    score: str
