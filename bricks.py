import pygame
from gameObject import GameObject
from config import BRICKSCOLOR, BRICKSWIDTH, BRICKSHEIGHT, WHITE


class Brick(GameObject):
    def __init__(self, x, y, image):
        GameObject.__init__(self, x, y, BRICKSWIDTH, BRICKSHEIGHT)
        self.color = BRICKSCOLOR
        self.image = image
        self.image = pygame.transform.scale(image, (BRICKSWIDTH, BRICKSHEIGHT))
        self.image.set_colorkey(WHITE)
