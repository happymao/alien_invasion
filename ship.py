import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # construction function for initialize class
    def __init__(self, ai_settings, screen):
        ''' initialize ship and ship's position '''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load ship.bmp and get rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # add ship.bmp into center bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # ship center attribute can store float
        self.center = float(self.rect.centerx)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        ''' move position of ship by moving flag '''

        # update ship center, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect by self.center
        self.rect.centerx = self.center

    def blitme(self):
        ''' draw ship in position'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        ''' let ship in center of bottom of screen '''
        self.center = self.screen_rect.centerx
