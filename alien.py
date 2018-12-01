import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    ''' signal alien class '''

    def __init__(self, ai_settings, screen):
        ''' initialize alien and his original position '''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load alien's image and set rectangle's attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # alien's original position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's position by float
        self.x = float(self.rect.x)

    # show alien
    def blitme(self):
        ''' draw alien on decided position '''
        self.screen.blit(self.image, self.rect)

    # check alien whether arrived edge
    def check_edges(self):
        ''' if alien arrived edge return True '''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    # alien moving
    def update(self):
        ''' move to right or left '''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
