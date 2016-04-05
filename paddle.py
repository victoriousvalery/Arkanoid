import pygame
import sys
from colours import *
from screen import *


PADDLE = 'paddle'


class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PADDLEWIDTH
        self.height = PADDLEHEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.name = PADDLE


    def update(self, movementx, *args):
        if self.rect.x >= 0 and self.rect.right <= DISPLAYWIDTH:
            self.rect.centerx = movementx

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH