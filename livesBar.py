import pygame
from colours import *
from screen import *


class LivesBar():
    def __init__(self):
        self.lives = AMOUNTOFLIVES
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.render = self.font.render('Lives: ' + str(self.lives), True, WHITE)
        self.rect = self.render.get_rect()
        self.rect.x = DISPLAYWIDTH * 0.86 # умножаю на коэффициент, чтобы подвинуть надпись с количеством оставшихся попыток
        self.rect.bottom = DISPLAYHEIGHT
        