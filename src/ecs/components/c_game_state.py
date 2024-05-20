from enum import Enum


class CGameState:
    def __init__(self):
        self.state = GameState.START


class GameState(Enum):
    UNPAUSED = 0
    PAUSED = 1
    DIED = 2
    OVER = 3
    START = 4
    CHANGE_LEVEL = 5
