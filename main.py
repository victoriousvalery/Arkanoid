import pygame
import os
import sys
from pygame.locals import *
from paddle import Paddle  # палка
from ball import Ball  # шар
from scoreBar import ScoreBar  # счетчик очков
from livesBar import LivesBar  # счетчик жизней
from levelBar import LevelBar  # счетчик уровня
from dataLoader import dataLoader  # загрузчик изображений
from block import Block  # блоки
from colours import *  # цвета
from screen import *  # константы
from button import Button  # кнопка
import levels  # уровни

# Палку увеличивать l*2, max размер = screen/2 - величина приза

time_to_wait = 1000 // Freq


class App(object):

    def __init__(self):
        pygame.init()
        self.currentLevel = 1
        self.displaySurf, self.displayRect = self.makeScreen()
        self.movementx = 0
        self.blocks = self.createBlocks(1)
        self.paddle = self.createPaddle()
        self.ball = self.createBall()
        self.level = LevelBar()
        self.score = ScoreBar()
        self.lives = LivesBar()
        self.allSprites = pygame.sprite.Group(
            self.blocks, self.paddle, self.ball)

    def updateScore(self):  # обновление надписи с очками
        self.score.score = self.ball.score
        self.score.render = self.score.font.render(
            'Score: ' + str(self.score.score), True, WHITE)
        self.score.rect = self.score.render.get_rect()
        self.score.rect.x = 0
        self.score.rect.bottom = DISPLAYHEIGHT

    def updateLevel(self):  # обновление надписи с данным уровнем
        self.level.level = self.currentLevel
        self.level.render = self.level.font.render(
            'Level: ' + str(self.level.level), True, WHITE)
        self.level.rect = self.level.render.get_rect()
        self.level.rect.x = DISPLAYWIDTH * 0.86
        self.level.rect.bottom = DISPLAYHEIGHT + 40

    def updateLives(self):  # обновление надписи с осташвимися попытками
        self.lives.lives = self.ball.lives
        self.lives.render = self.lives.font.render(
            'Lives: ' + str(self.lives.lives), True, WHITE)
        self.lives.rect = self.lives.render.get_rect()
        self.lives.rect.x = DISPLAYWIDTH * 0.86
        self.lives.rect.bottom = DISPLAYHEIGHT

    def makeScreen(self):  # экран во время игры
        pygame.display.set_caption('Arkanoid')
        displaySurf = pygame.display.set_mode(
            (DISPLAYWIDTH, DISPLAYHEIGHT))  # окно
        displayRect = displaySurf.get_rect()
        self.background_image = dataLoader().get_image(
            "backres.jpg")  # нормально написано?
        self.menu_image = dataLoader().get_image("menures.jpg")
        self.gameover_image = dataLoader().get_image("gameoverres.jpg")
        self.success_image = dataLoader().get_image("success.jpg")

        return displaySurf, displayRect

    def butStart(self):  # кнопка в основном меню
        self.startButton = Button("Start")
        self.startButton.draw(
            self.displaySurf, (310, 200, 170, 45), (365, 210))
        # self.startButton.check_hover(self.mouse)

    def createBall(self):  # создаем шар
        ball = Ball(self.displaySurf)
        ball.rect.centerx = self.paddle.rect.centerx
        ball.rect.bottom = self.paddle.rect.top

        return ball

    def createPaddle(self):  # создаем палку
        paddle = Paddle()
        paddle.rect.centerx = self.displayRect.centerx
        paddle.rect.bottom = self.displayRect.bottom

        return paddle

    def createBlocks(self, level):  # создаем блоки
        self.blocks = pygame.sprite.Group()
        self.infinityBlock = 0
        # не думаю, что будет хорошим тоном так обращаться к значению словаря
        for (y, row) in enumerate(levels.levels[level]):
            # однако пока ничего другого на ум не пришло
            for (x, column) in enumerate(row):
                # "парсим" словарь с уровнями
                if (column > "0" and column < "9") or column == "0":
                # берем число из строки и используем его для прочности
                    block = Block()
                    block.rect.x = x * BLOCKWIDTH + BLOCKGAP
                    block.rect.y = y * BLOCKHEIGHT + BLOCKGAP
                    #block.color = self.setBlockColor(block, row, column)
                    block.hardness = int(column)
                    # block.image.fill(block.color)
                    self.blocks.add(block)
                    if column == "0":
                    #непробиваемые блоки
                        self.infinityBlock += 1
                        block.image = dataLoader().get_image("ybbar.jpg")

        return self.blocks

    """def setBlockColor(self, block, row, column):  # цвет блоков -- это уберу
        if column == 0 or column % 2 == 0:
            return PURPLE
        else:
            return ORANGE"""

    # смотрим, как подвигали мышкой, какие стрелки нажали
    def checkInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()

            if event.type == MOUSEMOTION:  # двигаем мышку и перемещаем палку
                self.movementx = event.pos[0]

            elif event.type == KEYUP:  # стартуем по пробелу
                if event.key == K_SPACE:
                    self.ball.moving = True

            elif event.type == MOUSEBUTTONUP:  # стартуем по клику мышки
                self.ball.moving = True

    def terminate(self):  # выход
        pygame.quit()
        sys.exit()

    def mainLoop(self):
        while True:
            clicked = False
            # ждем, потому что CPU при запуске pygame на mac os x сильно
            # загружен
            pygame.time.wait(time_to_wait)
            # думаю, этой строчки в лупе не должно быть. Но как ее перенести?
            # (в инит?)
            self.menuButton = self.butStart()
            self.checkInput()  # проверяем ввод
            pygame.display.update()  # обновляем экран
            mouse = pygame.mouse.get_pos()
            # в этом лупе проверяем на нажатие кнопки "start" в меню
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.startButton.obj.collidepoint(mouse):
                        clicked = True
            # отрисовываем фоновую картинку
            self.displaySurf.blit(self.menu_image, [0, 0])

            while clicked:
            #цикл игрового процесса
                if self.ball.lives <= 0:  # выходим из цикла, если нет жизней
                    break
                if len(self.blocks) - self.infinityBlock > self.infinityBlock:  # если еще есть блоки
                    pygame.time.wait(time_to_wait)
                    self.updateScore()
                    self.updateLives()
                    self.updateLevel()
                    # фоновое изображение во время игры
                    self.displaySurf.blit(self.background_image, [0, 0])
                    self.displaySurf.blit(
                        self.score.render, self.score.rect)  # блитим счет
                    self.displaySurf.blit(
                        self.lives.render, self.lives.rect)  # блитим жизни
                    self.allSprites.update(
                        self.movementx, self.blocks, self.paddle)
                    # рисуем блоки, шар, палку
                    self.allSprites.draw(self.displaySurf)

                    # print(self.paddle.rect.centerx) # центр -- отладка
                    # print(self.paddle.rect.x) #левый -- отладка
                    # print(self.paddle.rect.right) #правый конец -- отладка

                    pygame.display.update()  # обновление экрана
                    self.checkInput()  # ввод
                # сюда заходим, если не осталось блоков. Переходим на следующий
                # уровень
                elif (self.currentLevel < len(levels.levels)):
                    # останавливаем шар и возвращаем его на место
                    self.ball.moving = False
                    self.ball.rect.centerx = self.paddle.rect.centerx
                    self.ball.rect.bottom = self.paddle.rect.top
                    # немного подождем, чтобы игрок собрался с силами
                    pygame.time.wait(1000)

                    self.currentLevel += 1
                    self.blocks = self.createBlocks(
                        self.currentLevel)  # генерим новые блоки
                    self.allSprites = pygame.sprite.Group(
                        self.blocks, self.paddle, self.ball)  # добавляем в спрайты
                    # можно ли здесь писать так? Или будет эффективнее использовать add?
                    # Или без разницы?
                    # рисуем блоки, шар, палку
                    self.allSprites.draw(self.displaySurf)
                    self.allSprites.update(
                        self.movementx, self.blocks, self.paddle)  # обновляем

                else:  # уровней не осталось, игра пройдена
                    self.displaySurf.blit(self.success_image, [0, 0])
                    pygame.display.update()
                    self.checkInput()

            # сюда мы заходим после брейка в while'е игры, чтобы вывести экран
            # GAME OVER
            if self.ball.lives <= 0:
                while True:
                    # рисуем экран game over
                    self.displaySurf.blit(self.gameover_image, [0, 0])
                    pygame.display.update()
                    self.checkInput()


if __name__ == '__main__':
    runGame = App()
    runGame.mainLoop()  # запуск основного лупа
