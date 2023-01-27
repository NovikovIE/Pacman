import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

    def left(self):
        return self.rect.left

    def right(self):
        return self.rect.right

    def top(self):
        return self.rect.top

    def bottom(self):
        return self.rect.bottom

    def center(self):
        return self.rect.center
