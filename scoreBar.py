import pygame
from colours import *
from screen import *



class ScoreBar():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.render = self.font.render('Score: ' + str(self.score), True, WHITE)
        self.rect = self.render.get_rect()
        self.rect.x = 0
        self.rect.bottom = DISPLAYHEIGHT