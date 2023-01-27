import pygame
from gameObject import GameObject
from config import BRICKSWIDTH, BRICKSHEIGHT, BLACK


class Teleport(GameObject):
    def __init__(self, x, y, is_left):
        GameObject.__init__(self, x, y, BRICKSWIDTH, BRICKSHEIGHT)
        self.is_left = is_left
