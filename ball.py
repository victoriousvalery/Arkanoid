import pygame
import math
import random
from block import Block
from colours import *  # цвета
from screen import *  # константы
# мне необходим этот импорт для того, чтобы после "улета" шарика вернуть
# его на место
from paddle import Paddle
# думаю, пригодится и еще


class Ball(pygame.sprite.Sprite):

    """Класс шара. Здесь обрабатываются столкновения, идет подсчет очков, меняется движение шара"""

    def __init__(self, displaySurf):
        pygame.sprite.Sprite.__init__(self)
        self.name = BALL
        self.moving = False
        self.image = pygame.Surface((15, 15))
        #self.image = pygame.draw.circle(displaySurf, RED, (300,200),1)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vectorx = BALLSPEED
        self.vectory = BALLSPEED * -1
        self.angle = 0.52
        self.score = 0
        self.lives = AMOUNTOFLIVES

    def update(self, movementx, blocks, paddle, *args):
        if not self.moving:
            self.rect.centerx = movementx

        else:
            self.rect.y += self.vectory * math.cos(self.angle)
            # таким образом, шар изначально улетает только в одну сторону(??)
            self.rect.x += self.vectorx * math.cos(self.angle)

            hitGroup = pygame.sprite.Group(paddle, blocks)

            spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)
            # обрабатываем столкновения шара с блоками
            if len(spriteHitList) > 0:
                for sprite in spriteHitList:
                    if sprite.name == BLOCK:
                        if sprite.hardness == 1:
                            sprite.kill()
                            self.score += 1
                        elif sprite.hardness == 0:
                            pass
                        else:
                            sprite.hardness -= 1
                # при отражении надо бы границах отражаемого объекта подумать
                self.vectory *= -1
                self.rect.y += self.vectory

            blockHitList = pygame.sprite.spritecollide(self, blocks, True)

            if len(blockHitList) > 0:
                self.vectorx *= -1
                self.score += 1

            if self.rect.right > DISPLAYWIDTH:
                self.vectorx *= -1
                self.rect.right = DISPLAYWIDTH

            elif self.rect.left < 0:
                self.vectorx *= -1
                self.rect.left = 0

            if self.rect.top < 0:  # если улетает вверх
                self.vectory *= -1
                self.rect.top = 0

            if self.rect.top > DISPLAYHEIGHT:  # если улетает вниз
                self.lives -= 1
                self.moving = False
                self.rect.centerx = paddle.rect.centerx
                self.rect.bottom = paddle.rect.top
