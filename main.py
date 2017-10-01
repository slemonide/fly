import pygame, sys
from world import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_HEIGHT = 20


def draw_statusbar(display):
    pygame.draw.rect(display, pygame.Color("red"), pygame.Rect(0, 0, SCREEN_WIDTH, TEXT_HEIGHT))


def render_world(display):
    display.fill((0, 0, 0))

    draw_statusbar(display)

    player = pygame.image.load("assets/player.png")

    display.blit(player, player.get_rect().move((SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)))
    pygame.display.flip()


def quit_game():
    pygame.quit()
    sys.exit()


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()


def update_environment():
    pass


def main():
    pygame.init()
    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    world = World()

    while True:
        render_world(display)
        handle_input()
        update_environment()


if __name__ == '__main__':
    main()
