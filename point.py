import pygame
from config import POINTCOLOR, POINTRADIUS, BLACK
from gameObject import GameObject


class Point(GameObject):
    def __init__(self, x, y, image):
        GameObject.__init__(self, x - POINTRADIUS, y - POINTRADIUS, 2 * POINTRADIUS, 2 * POINTRADIUS)
        self.radius = POINTRADIUS
        self.color = POINTCOLOR
        self.image = image
        self.image = pygame.transform.scale(image, (2 * self.radius, 2 * self.radius))
        self.image.set_colorkey(BLACK)
