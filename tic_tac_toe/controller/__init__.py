"""Контроллер: связывает действия пользователя с моделью и представлением."""

from tic_tac_toe.controller.game_controller import GameController
from tic_tac_toe.controller.view_protocol import GameView
from tic_tac_toe.controller.view_state import ViewState

__all__ = ["GameController", "GameView", "ViewState"]
