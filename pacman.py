import pygame
from dynamicObject import DynamicObject
from config import PACMANWIDTH, PACMANHEIGHT, PACMANLIVES, BLACK


class Pacman(DynamicObject):
    def __init__(self, x, y, images):
        DynamicObject.__init__(self, x, y, PACMANWIDTH, PACMANHEIGHT)
        self.score = 0
        self.lives = PACMANLIVES
        self.direction = "horizontal"
        self.images = []
        for i in range(len(images)):
            self.images.append(pygame.transform.scale(images[i], (PACMANWIDTH, PACMANHEIGHT)))
            self.images[i].get_rect().center = self.rect.center
        self.image = self.images[3]
        self.image.set_colorkey(BLACK)
        self.condition = 0
        self.direction = "NONE"

    # opens or closes mouth if necessary and changes image if previous direction is not equal to present direction
    def move_mouth(self, index):
        if self.image == self.images[index]:
            if self.condition >= 10:
                self.condition = 0
                self.image = self.images[index + 1]
            else:
                self.condition += 1
        elif self.image == self.images[index + 1]:
            if self.condition >= 10:
                self.condition = 0
                self.image = self.images[index]
            else:
                self.condition += 1
        else:
            self.condition = 0
            self.image = self.images[index]

    # moves pacman
    def update(self):
        if self.direction == "LEFT":
            self.move_mouth(0)
            self.move_left()
        elif self.direction == "UP":
            self.move_mouth(2)
            self.move_up()
        elif self.direction == "DOWN":
            self.move_mouth(6)
            self.move_down()
        elif self.direction == "RIGHT":
            self.move_mouth(4)
            self.move_right()
        self.image.set_colorkey(BLACK)

    def add_point(self):
        self.score += 1
