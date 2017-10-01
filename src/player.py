import pygame
import math

from .space_body import SpaceBody

ACCELERATION = 0.1
ROTATION_SPEED = 0.1


class Player(SpaceBody):
    def __init__(self):
        super().__init__(0, 0)
        self.vt = 1
        self.t = 0

        self.rotation = 0

        self.image = pygame.image.load("assets/player.png")

    pass

    def thrust_forward(self):
        self.x += ACCELERATION * math.cos(self.rotation)
        self.y += ACCELERATION * math.cos(self.rotation)

    def thrust_backwards(self):
        self.x -= ACCELERATION * math.cos(self.rotation)
        self.y -= ACCELERATION * math.cos(self.rotation)

    def rotate_right(self):
        self.rotation -= ROTATION_SPEED

        self.update_sprite()

    def rotate_left(self):
        self.rotation += ROTATION_SPEED

        self.update_sprite()

    def update_sprite(self):
        pass

    def update(self, dt):
        super(Player, self).update(dt)

        self.t += dt
