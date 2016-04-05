import pygame
from colours import *
from screen import *
"""Класс для отображения текущего уровня в игре"""

class LevelBar():
    def __init__(self):
        self.level = 1
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.render = self.font.render('Level: ' + str(self.level), True, WHITE)
        self.rect = self.render.get_rect()
        self.rect.x = DISPLAYWIDTH * 0.86 
        self.rect.bottom = DISPLAYHEIGHT + 25 
        