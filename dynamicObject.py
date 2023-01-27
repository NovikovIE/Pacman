from gameObject import GameObject
from config import SPEED


class DynamicObject(GameObject):
    def __init__(self, x, y, width, height):
        GameObject.__init__(self, x, y, width, height)
        self.direction = "horizontal"
        self.speed = SPEED

    def move_left(self):
        self.rect.x -= self.speed
        self.direction = "horizontal"

    def move_right(self):
        self.rect.x += self.speed
        self.direction = "horizontal"

    def move_up(self):
        self.rect.y -= self.speed
        self.direction = "vertical"

    def move_down(self):
        self.rect.y += self.speed
        self.direction = "vertical"
