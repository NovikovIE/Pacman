import pygame
from gameObject import GameObject


class Button(GameObject):
    def __init__(self, x, y, width, height, color):
        GameObject.__init__(self, x, y, width, height)
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)