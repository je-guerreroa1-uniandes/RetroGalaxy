from enum import Enum

class CTagEnemy:
    def __init__(self, type:str)->None:
        self.type = type
        self.state = EnemyState.MOVING

class EnemyState(Enum):
    MOVING = 0
    ROTATING = 1
    CHASE = 2