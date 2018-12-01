import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from game_stats import GameStats
from score_board import Scoreboard


def run_game():
    # initialize a game window
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # create Play button
    play_button = Button(ai_settings, screen, "Play")

    # create initial data object
    stats = GameStats(ai_settings)

    # create a ship
    ship = Ship(ai_settings, screen)
    # create bullet's group
    bullets = Group()
    # create an alien guoup
    aliens = Group()

    # create a group alien
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create statistic instance and score board
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # start game main loop
    while True:
        # verify keyboard and mouse event
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
