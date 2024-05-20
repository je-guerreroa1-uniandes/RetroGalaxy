import pygame
from enum import Enum

class CAlien:
    def __init__(self, posObj:pygame.Vector2, velActual_x:int):
        self.posObj = posObj
        self.rotation = 0
        self.state = AlienState.MOV
        self.velActual_x = velActual_x

class AlienState(Enum):
    MOV = 0
    CHASE = 1
    RETURN = 2