import pygame


class CStar:
    def __init__(self, time:float, color:pygame.Color) -> None:
        self.state = 1
        self.timeAlive = 0
        self.time = time
        self.color = color