import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    ''' create a class for manage buller '''

    def __init__(self, ai_settings, screen, ship):
        ''' create a bullet on the position of ship '''
        super(Bullet, self).__init__()  # otherwise Super __init__() will be over written
        self.screen = screen

        # create a rectangle on position(0,0), then pose it on correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store bullet's position by float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

        # sound of bullet todo

    def update(self):
        ''' move bullet to top '''

        # update position by float
        self.y -= self.speed_factor
        # update bullet's rect position
        self.rect.y = self.y

    def draw_bullet(self):
        ''' draw bullet on the screen '''
        pygame.draw.rect(self.screen, self.color, self.rect)
