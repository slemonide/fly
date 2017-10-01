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

        self.rotation = math.pi/2

        self.up_image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.rotate(self.up_image, self.rotation * 180/math.pi)

    def thrust_forward(self):
        self.vx += ACCELERATION * math.cos(self.rotation)
        self.vy += ACCELERATION * math.sin(self.rotation)

    def thrust_backwards(self):
        self.vx -= ACCELERATION * math.cos(self.rotation)
        self.vy -= ACCELERATION * math.sin(self.rotation)

    def rotate_right(self):
        self.rotation -= ROTATION_SPEED

        self.update_sprite()

    def rotate_left(self):
        self.rotation += ROTATION_SPEED

        self.update_sprite()

    def update_sprite(self):
        self.image = pygame.transform.rotate(self.up_image, self.rotation * 180/math.pi)

    def update(self, dt):
        super(Player, self).update(dt)

        self.t += dt
