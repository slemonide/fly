import math
import sys
from os import path, getcwd

from camera import *
from nanogui import Nanogui

class Game:
    # Treat Game as singleton
    instance = None

    def __init__(self, display):
        Game.instance = self

        self.display = display
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)

        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        self.joystick = None
        if len(self.joysticks) > 0:
            self.joystick = self.joysticks[0]
            self.joystick.init()

        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.solid = pg.sprite.Group()
        self.items_on_floor = pg.sprite.Group()
        self.doors = pg.sprite.Group()

        self.background_surface = None
        self.collisions = []  # rectangles
        self.spritesheet = None
        self.map = None
        self.player = None
        self.camera = None
        self.playing = False
        self.dt = 0.0
        self.global_time = 0
        self.pressed_keys = {}
        self.keys_just_pressed = {}
        self.joystick_just_pressed = {}

        self.gui = Nanogui(display)
        self.visibility_data = None  # [x][y] -> True, False
        self.fov_data = None  # [x][y] -> True, False
        self.update_fov = True
        self.light_map = []

    def load(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def __put_picture_on_screen(self, image):
        self.display.blit(image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.global_time += self.dt
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        self.keys_just_pressed.clear()
        self.joystick_just_pressed.clear()

        self.pressed_keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                self.keys_just_pressed[event.key] = True
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F11:
                    self.toggle_fullscreen()
            if event.type == pg.JOYBUTTONDOWN:
                self.joystick_just_pressed[event.button] = True

    def toggle_fullscreen(self):
        """Taken from http://pygame.org/wiki/toggle_fullscreen"""

        screen = pg.display.get_surface()
        tmp = screen.convert()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()

        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        self.display = pg.display.set_mode((w, h), flags ^ pg.FULLSCREEN, bits)
        self.display.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)

        pg.key.set_mods(0)

        pg.mouse.set_cursor(*cursor)

        return screen

    def get_vbutton_down(self, name):
        if name in V_BUTTONS:
            for key in V_BUTTONS[name]:
                if self.pressed_keys[key]:
                    return True
        return False

    def get_vbutton_jp(self, name):
        if name in V_BUTTONS:
            for key in V_BUTTONS[name]:
                if key in self.keys_just_pressed:
                    return True
        return False

    def get_key_jp(self, key):
        # get key just pressed (clears on new frame)
        if key in self.keys_just_pressed:
            return True
        return False

    def get_joystick_jp(self, button):
        # get joystick button just pressed (clears on new frame)
        if button in self.joystick_just_pressed:
            return True
        return False

    def get_axis(self, number):
        if self.joystick is not None:
            return self.joystick.get_axis(number)
        return 0.0

    def set_visibility(self, tilex, tiley, value):
        self.visibility_data[tilex][tiley] = value
        self.update_fov = True

    def draw_fov(self):
        for x in range(len(self.fov_data)):
            for y in range(len(self.fov_data[0])):
                if self.fov_data[x][y]:
                    newx, newy = self.camera.transform_xy(x * TILE_SIZE, y * TILE_SIZE)
                    pg.draw.rect(self.display, (200, 200, 200), pg.Rect(newx, newy,
                                                                        TILE_SIZE, TILE_SIZE), 1)

    def update_light_map(self, source_x, source_y):
        self.light_map.clear()
        radius_sqr = FOV_RADIUS * FOV_RADIUS
        tmp = 1.0 / (1.0 + radius_sqr)

        for x in range(len(self.fov_data)):
            for y in range(len(self.fov_data[0])):
                if self.fov_data[x][y]:
                    newx, newy = self.camera.transform_xy(x * TILE_SIZE, y * TILE_SIZE)

                    dist_sqr = (source_x - x)*(source_x - x) + (source_y - y)*(source_y - y)
                    intensity = 1.0 / (1.0 + dist_sqr / 20)
                    intensity = intensity - tmp
                    intensity = intensity / (1.0 - tmp)
                    color = tuple(intensity*v for v in LIGHT_COLOR)
                    self.light_map.append((pg.Rect(newx, newy, TILE_SIZE, TILE_SIZE), color))
