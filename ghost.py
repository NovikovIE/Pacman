import pygame
from dynamicObject import DynamicObject
from config import GHOSTHEIGHT, GHOSTWIDTH, STARTMAPWIDTH, BRICKSWIDTH, BRICKSHEIGHT, BLACK
from graph import Vertex


class Ghost(DynamicObject):
    def __init__(self, x, y, images):
        DynamicObject.__init__(self, x, y, GHOSTWIDTH, GHOSTHEIGHT)
        self.direction = "horizontal"
        self.is_active = False
        self.path = [Vertex(STARTMAPWIDTH + int(BRICKSWIDTH * 16), BRICKSHEIGHT * 12)]
        self.cur = 0
        self.previous_direction = "LEFT"
        self.collision = False
        self.time_for_non_searching_pacman = 0
        self.is_new_path = False
        self.images = []
        for i in range(len(images)):
            self.images.append(pygame.transform.scale(images[i], (GHOSTWIDTH, GHOSTHEIGHT)))
        self.image = self.images[0]
        self.image.set_colorkey(BLACK)

    # updates image based on direction
    def update_image(self):
        if self.previous_direction == "LEFT":
            self.image = self.images[0]
        elif self.previous_direction == "UP":
            self.image = self.images[1]
        elif self.previous_direction == "RIGHT":
            self.image = self.images[2]
        elif self.previous_direction == "DOWN":
            self.image = self.images[3]
        self.image.set_colorkey(BLACK)

    # changes path (usually searches path from position in current path,
    # but if path is empty it watches on node where ghost is)
    def change_path(self, x, y, graph, vertices):
        try:
            start = self.path[self.cur]
        except:
            start = -1
        if start == -1 or self.is_new_path:
            self.is_new_path = False
            objects = pygame.sprite.spritecollide(self, vertices, False)
            if len(objects) == 1:
                for obj in objects:
                    start = obj
            else:
                for obj in objects:
                    if obj.rect.x < self.rect.x and self.previous_direction != "RIGHT":
                        if obj.rect.y < self.rect.y and self.previous_direction != "DOWN":
                            start = obj
                        elif obj.rect.y > self.rect.y and self.previous_direction != "UP":
                            start = obj
                    elif obj.rect.x < self.rect.x and self.previous_direction != "LEFT":
                        if obj.rect.y < self.rect.y and self.previous_direction != "DOWN":
                            start = obj
                        elif obj.rect.y > self.rect.y and self.previous_direction != "UP":
                            start = obj
                if start == -1 or start == self.path[self.cur]:
                    start = objects[0]
        self.path = graph.find_path(graph.vertices_by_coords[(start.rect.x, start.rect.y)],
                                    graph.vertices_by_coords[(x, y)])
        self.cur = 0

    # changes direction on opposite
    def change_direction(self):
        if self.previous_direction == "LEFT":
            self.previous_direction = "RIGHT"
        elif self.previous_direction == "RIGHT":
            self.previous_direction = "LEFT"
        elif self.previous_direction == "UP":
            self.previous_direction = "LEFT"
        elif self.previous_direction == "DOWN":
            self.previous_direction = "LEFT"

    def tick(self):
        self.time_for_non_searching_pacman += 1

    # moves linear for a short time after collision with another ghost
    def linear_movement(self):
        if self.collision:
            self.tick()
        if self.previous_direction == "LEFT":
            self.move_left()
        elif self.previous_direction == "RIGHT":
            self.move_right()
        elif self.previous_direction == "UP":
            self.move_up()
        elif self.previous_direction == "DOWN":
            self.move_down()

    # goes through path
    def go_to_pacman(self):
        if self.time_for_non_searching_pacman >= 120:
            self.time_for_non_searching_pacman = 0
            self.collision = False
            self.is_new_path = True
        if self.collision or len(self.path) == 0 or self.rect.center == self.path[len(self.path) - 1].rect.center:
            self.linear_movement()
            self.update_image()
            return 0
        if self.path[self.cur].rect.center == self.rect.center:
            if self.cur < len(self.path) - 1:
                self.cur += 1
        diff_x = self.path[self.cur].rect.centerx - self.rect.centerx
        diff_y = self.path[self.cur].rect.centery - self.rect.centery
        if diff_x:
            if diff_x <= 0:
                self.previous_direction = "LEFT"
                if abs(self.rect.centerx - self.path[self.cur].rect.centerx) < self.speed:
                    self.rect.centerx = self.path[self.cur].rect.centerx
                else:
                    self.move_left()
            else:
                self.previous_direction = "RIGHT"
                if abs(self.path[self.cur].rect.centerx - self.rect.centerx) < self.speed:
                    self.rect.centerx = self.path[self.cur].rect.centerx
                else:
                    self.move_right()
        else:
            if diff_y <= 0:
                self.previous_direction = "UP"
                if abs(self.rect.centery - self.path[self.cur].rect.centery) < self.speed:
                    self.rect.centery = self.path[self.cur].rect.centery
                else:
                    self.move_up()
            else:
                self.previous_direction = "DOWN"
                if abs(self.path[self.cur].rect.centery - self.rect.centery) < self.speed:
                    self.rect.centery = self.path[self.cur].rect.centery
                else:
                    self.move_down()
        self.update_image()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
