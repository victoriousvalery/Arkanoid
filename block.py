import pygame
import sys
from colours import *
from screen import *
from dataLoader import dataLoader
"""Класс блоков"""

BLOCK = 'block'


class Block(pygame.sprite.Sprite): #этот класс должен быть в отдельном файле

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.blockWidth = BLOCKWIDTH
        self.blockHeight = BLOCKHEIGHT
        self.image = pygame.Surface((self.blockWidth, self.blockHeight))
        self.image = dataLoader().get_image("bar.png") # рисунок для наших блоков
        self.rect = self.image.get_rect()
        self.name = BLOCK
        self.hardness = 1