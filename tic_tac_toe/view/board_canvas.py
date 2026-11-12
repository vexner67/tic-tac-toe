"""Холст, на котором рисуется игровое поле."""

import tkinter as tk
from typing import Callable, Optional

from tic_tac_toe.controller import ViewState
from tic_tac_toe.model import BOARD_SIZE, Position
from tic_tac_toe.view import theme
from tic_tac_toe.view.geometry import BoardGeometry

CellHandler = Callable[[int, int], None]


class BoardCanvas(tk.Canvas):
    """Масштабируемое поле: перерисовывается при изменении размера окна."""

    def __init__(self, master: tk.Misc, on_cell_click: CellHandler) -> None:
        super().__init__(master, background=theme.BACKGROUND,
                         highlightthickness=0)
        self._on_cell_click = on_cell_click
        self._state: Optional[ViewState] = None
        self.bind("<Configure>", lambda _event: self._redraw())
        self.bind("<Button-1>", self._handle_click)

    def show(self, state: ViewState) -> None:
        """Запомнить новое состояние и перерисовать поле."""
        self._state = state
        self.configure(cursor="arrow" if state.locked else "hand2")
        self._redraw()

    def _geometry(self) -> BoardGeometry:
        return BoardGeometry(self.winfo_width(), self.winfo_height(),
                             BOARD_SIZE)

    def _handle_click(self, event: tk.Event) -> None:
        cell = self._geometry().cell_at(event.x, event.y)
        if cell is not None:
            self._on_cell_click(*cell)

    def _redraw(self) -> None:
        self.delete("all")
        if self._state is None:
            return
        geometry = self._geometry()
        for row, line in enumerate(self._state.cells):
            for col, symbol in enumerate(line):
                self._draw_cell(geometry, row, col, symbol)

    def _draw_cell(self, geometry: BoardGeometry, row: int, col: int,
                   symbol: str) -> None:
        rect = geometry.cell_rect(row, col)
        highlighted = Position(row, col) in self._state.highlighted
        self.create_rectangle(
            *rect, outline=theme.GRID, width=theme.GRID_WIDTH,
            fill=theme.CELL_HIGHLIGHT if highlighted else theme.BACKGROUND,
        )
        if symbol == "X":
            self._draw_x(rect, geometry.cell)
        elif symbol == "O":
            self._draw_o(rect, geometry.cell)

    def _draw_x(self, rect: tuple, cell: float) -> None:
        x1, y1, x2, y2 = _shrink(rect, cell * theme.MARK_PADDING_RATIO)
        width = max(cell * theme.MARK_WIDTH_RATIO, 1)
        for line in ((x1, y1, x2, y2), (x1, y2, x2, y1)):
            self.create_line(*line, fill=theme.X_COLOR, width=width,
                             capstyle=tk.ROUND)

    def _draw_o(self, rect: tuple, cell: float) -> None:
        width = max(cell * theme.MARK_WIDTH_RATIO, 1)
        self.create_oval(*_shrink(rect, cell * theme.MARK_PADDING_RATIO),
                         outline=theme.O_COLOR, width=width)


def _shrink(rect: tuple, padding: float) -> tuple:
    """Уменьшить прямоугольник на ``padding`` с каждой стороны."""
    x1, y1, x2, y2 = rect
    return x1 + padding, y1 + padding, x2 - padding, y2 - padding
