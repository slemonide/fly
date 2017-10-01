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
FPS = 60
SCALE = 20 # 1 lsec is 20 pixels


class Game:
    game = None

    def __init__(self):
        self.controls = {"up": False,
                         "down": False,
                         "left": False,
                         "right": False}
        Game.game = self

        pygame.init()
        pygame.mixer.music.load("assets/music/420.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.Font("assets/fonts/unifont-10.0.06.ttf", TEXT_HEIGHT)
        self.world = World()
        self.player = Player()

        Asteroid(10, 10)
        Asteroid(5, 5)

    def run(self):
        while True:
            self.render_world(self.display)
            self.handle_input()
            self.update_environment()

    def draw_statusbar(self, display):
        pygame.draw.rect(display, pygame.Color(191, 87, 0), pygame.Rect(0, 0, SCREEN_WIDTH, TEXT_HEIGHT + 5))

        surface = self.font.render("Time: " + str("%.1f" % self.player.t) + " seconds | " +
                                   "x: " + "%.1f"%self.player.x + " light seconds | " +
                                   "y: " + "%.1f"%self.player.y + " light seconds"

                                   , True, (144, 238, 144))
        self.display.blit(surface, (0, 0))

    def render_world(self, display):
        display.fill((0, 0, 0))

        self.draw_statusbar(display)

        for body in SpaceBody.space_bodies:
            display.blit(body.image, body
                         .image.get_rect()
                         .move((body.x - self.player.x)*SCALE - body.image.get_rect().width/2 + SCREEN_WIDTH/2,
                               (-body.y + self.player.y)*SCALE - body.image.get_rect().height/2 + SCREEN_HEIGHT/2))

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
                    self.controls["up"] = True
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = True
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = True
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.controls["up"] = False
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = False
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = False
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = False

    def update_environment(self):
        dt = self.clock.tick(FPS) / 1000

        if self.controls["up"]:
            self.player.thrust_forward()
        if self.controls["down"]:
            self.player.thrust_backwards()
        if self.controls["right"]:
            self.player.rotate_right()
        if self.controls["left"]:
            self.player.rotate_left()

        for body in SpaceBody.space_bodies:
            body.update(dt)
