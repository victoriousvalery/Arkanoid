import pygame
import os
import sys


class dataLoader:

    """Этот класс используется для загрузки изображений. Сделан для того, чтобы не плодить в программе try-catch блоки"""

    # здесь явно что-то не так с инитом
    def __init__(self, data_folder="data", image="images"):
        self.data_folder = data_folder
        self.image = image

    def get_image(self, name):
        fullpath = os.path.join(
            self.data_folder, os.path.join(self.image, name))
        try:
            image = pygame.image.load(fullpath)
        except RuntimeError:
            print(
                "Something went wrong while trying to load the image: %s" % name , file=sys.stderr)
            raise SystemExit
        else:
            image = image.convert()
            return image
