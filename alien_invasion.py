import sys
import pygame

from settings import Settings


def run_game():
    # initialize a game window
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # start game main loop
    while True:
        # verify keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # redraw window with back ground color
        screen.fill(ai_settings.bg_color)

        # show window
        pygame.display.flip()

run_game()
