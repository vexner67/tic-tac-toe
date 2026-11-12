"""Точка сборки приложения: создание модели, представления и контроллера."""

import tkinter as tk

from tic_tac_toe.controller import GameController
from tic_tac_toe.model import Match
from tic_tac_toe.view import MainWindow


def run() -> None:
    """Собрать компоненты MVC и запустить приложение."""
    window = MainWindow(tk.Tk())
    controller = GameController(Match(), window)
    window.attach(controller)
    controller.start()
    window.run()
