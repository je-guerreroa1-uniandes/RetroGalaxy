

import pygame


class FontsService:
    def __init__(self):
        self.fonts = {}

    def get(self, path:str, size:int) -> pygame.font.Font:
        
        if path not in self.fonts:
            self.fonts[path] = pygame.font.Font(path, size)

        return self.fonts[path]