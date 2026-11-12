"""Геометрия поля на холсте: перевод пикселей в клетки и обратно.

Модуль не зависит от tkinter и поэтому полностью покрыт тестами.
"""

from dataclasses import dataclass
from typing import Optional

#: Прямоугольник ``(x1, y1, x2, y2)`` в пикселях.
Rect = tuple[float, float, float, float]


@dataclass(frozen=True)
class BoardGeometry:
    """Квадратное поле, вписанное по центру в холст ``width × height``."""

    width: int
    height: int
    size: int
    margin: int = 10

    @property
    def side(self) -> float:
        """Длина стороны поля в пикселях."""
        return max(min(self.width, self.height) - 2 * self.margin, 0)

    @property
    def cell(self) -> float:
        """Длина стороны одной клетки в пикселях."""
        return self.side / self.size

    @property
    def origin(self) -> tuple[float, float]:
        """Координаты левого верхнего угла поля."""
        return (self.width - self.side) / 2, (self.height - self.side) / 2

    def cell_at(self, x: float, y: float) -> Optional[tuple[int, int]]:
        """Клетка ``(row, col)`` под точкой или ``None`` вне поля."""
        if self.cell == 0:
            return None
        left, top = self.origin
        col = int((x - left) // self.cell)
        row = int((y - top) // self.cell)
        if 0 <= row < self.size and 0 <= col < self.size:
            return row, col
        return None

    def cell_rect(self, row: int, col: int) -> Rect:
        """Прямоугольник клетки ``(row, col)``."""
        left, top = self.origin
        x1 = left + col * self.cell
        y1 = top + row * self.cell
        return x1, y1, x1 + self.cell, y1 + self.cell
