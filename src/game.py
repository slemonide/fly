import pygame
import sys
import datetime
from src.asteroid import *
from src.player import *
from src.world import World
from src.space_body import SpaceBody

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_HEIGHT = 20
FPS = 25


class Game:
    game = None

    def __init__(self):
        Game.game = self

        pygame.init()
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.Font("assets/fonts/unifont-10.0.06.ttf", TEXT_HEIGHT)
        self.world = World()
        self.player = Player()

        self.all_objects = []
        self.asteroids = []

        Asteroid(10, 10)
        Asteroid(5, 5)

    def run(self):
        while True:
            self.render_world(self.display)
            self.handle_input()
            self.update_environment()

    def draw_statusbar(self, display):
        pygame.draw.rect(display, pygame.Color(200, 100, 40), pygame.Rect(0, 0, SCREEN_WIDTH, TEXT_HEIGHT + 5))

        surface = self.font.render("Time: " + str(self.player.t) + " seconds | " +
                                   "x: " + str(self.player.x) + " light seconds | " +
                                   "y: " + str(self.player.y) + " light seconds"

                                   , True, (50, 100, 255))
        self.display.blit(surface, (0, 0))

    def render_world(self, display):
        display.fill((0, 0, 0))

        self.draw_statusbar(display)

        display.blit(self.player.image, self.player.image.get_rect().move((SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)))

        for asteroid in self.asteroids:
            display.blit(asteroid.image, asteroid
                         .image.get_rect()
                         .move(asteroid.x - self.player.x,
                               asteroid.y - self.player.y))

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()

                if event.key == pygame.K_UP:
                    self.player.thrust_forward()
                if event.key == pygame.K_DOWN:
                    self.player.thrust_backwards()
                if event.key == pygame.K_RIGHT:
                    self.player.rotate_right()
                if event.key == pygame.K_LEFT:
                    self.player.rotate_left()

    def update_environment(self):
        dt = self.clock.tick(FPS) / 1000

        for body in SpaceBody.space_bodies:
            body.update(dt)
