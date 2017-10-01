import pygame

from src.space_body import SpaceBody


class Asteroid(SpaceBody):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/asteroid.png")