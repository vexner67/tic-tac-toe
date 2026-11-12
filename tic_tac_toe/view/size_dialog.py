"""Диалог ввода произвольного размера окна."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tic_tac_toe.model import WindowSize

#: Обработчик ввода: получает строки ширины и высоты и возвращает
#: ``True``, если размер принят и диалог можно закрыть.
SubmitHandler = Callable[[str, str], bool]


class WindowSizeDialog(tk.Toplevel):
    """Модальное окно с полями «Ширина» и «Высота»."""

    def __init__(self, master: tk.Misc, current: WindowSize,
                 on_submit: SubmitHandler) -> None:
        super().__init__(master)
        self.title("Размер окна")
        self.resizable(False, False)
        self.transient(master)
        self._on_submit = on_submit
        self._width = tk.StringVar(value=str(current.width))
        self._height = tk.StringVar(value=str(current.height))
        self._build()
        self.bind("<Return>", lambda _event: self._submit())
        self.bind("<Escape>", lambda _event: self.destroy())
        self.grab_set()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.grid()
        hint = (f"Ширина: {WindowSize.MIN_WIDTH}–{WindowSize.MAX_WIDTH}, "
                f"высота: {WindowSize.MIN_HEIGHT}–{WindowSize.MAX_HEIGHT}")
        ttk.Label(frame, text=hint).grid(row=0, column=0, columnspan=2,
                                         pady=(0, 8))
        for row, (label, variable) in enumerate(
                (("Ширина:", self._width), ("Высота:", self._height)),
                start=1):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
            entry = ttk.Entry(frame, textvariable=variable, width=10)
            entry.grid(row=row, column=1, pady=2)
            if row == 1:
                entry.focus_set()
        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(buttons, text="Применить",
                   command=self._submit).grid(row=0, column=0, padx=4)
        ttk.Button(buttons, text="Отмена",
                   command=self.destroy).grid(row=0, column=1, padx=4)

    def _submit(self) -> None:
        if self._on_submit(self._width.get(), self._height.get()):
            self.destroy()
