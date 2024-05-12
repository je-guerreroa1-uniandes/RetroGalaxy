from enum import Enum


class CGameState:
    def __init__(self):
        self.state = GameState.UNPAUSED


class GameState(Enum):
    UNPAUSED = 0
    PAUSED = 1
