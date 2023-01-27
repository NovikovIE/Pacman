import pygame
from config import *
from pacman import Pacman
from ghost import Ghost
from bricks import Brick
from point import Point
from timer import Timer
from teleport import Teleport
from graph import Graph
from interface import Interface
from menu import Menu
import os


class PacmanGame:
    def __init__(self):
        game_folder = os.path.dirname(__file__)
        self.map_number = 0
        self.img_folder = os.path.join(game_folder, "img")
        self.frame_rate = FRAMERATE
        self.interface = Interface("Pacman", WIN_WIDTH, WIN_HEIGHT)
        self.brick_image = pygame.image.load(os.path.join(self.img_folder, "brick.png")).convert()
        self.point_image = pygame.image.load(os.path.join(self.img_folder, "point.png")).convert()
        self.timer = Timer(self.frame_rate)
        self.initialize_ghost_images()
        self.initialize_pacman_image()
        self.menu = Menu()
        self.restart()

    def restart(self):
        self.pacman = Pacman(STARTPACMANPOSITION[0], STARTPACMANPOSITION[1], self.pacman_images)
        self.pacman.score = 0
        self.pacman.lives = 3
        self.timer.reset_time()
        self.pacman.rect.x = STARTPACMANPOSITION[0]
        self.pacman.rect.y = STARTPACMANPOSITION[1]
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pacman)
        self.pacman_position = [(STARTPACMANPOSITION[0], STARTPACMANPOSITION[1])]
        self.initialize_map()
        self.running = True
        self.win = False
        self.loss = False
        self.stop = False

    # gets ghost sprites(in different directions)
    def initialize_ghost_images(self):
        self.ghosts_images = []
        for color in ["blue", "red", "pink", "orange"]:
            one_ghost = []
            for direction in ["left", "up", "right", "down"]:
                ghost_image = pygame.image.load(
                    os.path.join(self.img_folder, color + "_ghost_" + direction + ".png")).convert()
                one_ghost.append(ghost_image)
            self.ghosts_images.append(one_ghost)

    # gets pacman sprites(in different directions)
    def initialize_pacman_image(self):
        self.pacman_images = []
        for direction in ["left1", "left2", "up1", "up2", "right1", "right2", "down1", "down2"]:
            pacman_image = pygame.image.load(
                os.path.join(self.img_folder, "pacman_" + direction + ".png")).convert()
            self.pacman_images.append(pacman_image)

    # adds edge if suitable
    def try_to_add_edge(self, j, i, count):
        if j != 0:
            if MAP[self.map_number][i][j - 1] == 2 or MAP[self.map_number][i][j - 1] == 0:
                self.graph.add_edge(count, self.graph.vertices_by_coords[
                    (STARTMAPWIDTH + BRICKSWIDTH * (j - 1), BRICKSHEIGHT * i)])
        if i != 0:
            if MAP[self.map_number][i - 1][j] == 2 or MAP[self.map_number][i - 1][j] == 0:
                self.graph.add_edge(count, self.graph.vertices_by_coords[
                    (STARTMAPWIDTH + BRICKSWIDTH * j, BRICKSHEIGHT * (i - 1))])

    # adds node(vertex) to graph
    def add_node(self, j, i):
        self.graph.add_vertex(self.count, STARTMAPWIDTH + BRICKSWIDTH * j, BRICKSHEIGHT * i)
        self.vertices.add(self.graph.nodes[self.count])
        self.try_to_add_edge(j, i, self.count)
        self.count += 1

    # initializes map
    def initialize_map(self):
        self.bricks = pygame.sprite.Group()
        self.points = pygame.sprite.Group()
        self.teleports = pygame.sprite.Group()
        self.ghosts_sprites = pygame.sprite.Group()
        self.vertices = pygame.sprite.Group()
        self.graph = Graph(GRAPHLENGTH[self.map_number])
        self.ghosts = []
        self.count = 0
        for i in range(len(MAP[self.map_number])):
            for j in range(len(MAP[self.map_number][i])):
                element = MAP[self.map_number][i][j]
                # element:
                # 0 - point
                # 1 - brick
                # 2 - space without visible objects where pacman can go
                # 3, 4 - left and right teleport
                # 5 - space where pacman and other entities cannot go
                # 6, 7, 8, 9 - first, second, third and fourth ghosts
                if element == 0:
                    point = Point(STARTMAPWIDTH + BRICKSWIDTH * j + (BRICKSWIDTH // 2),
                                  BRICKSHEIGHT * i + (BRICKSWIDTH // 2), self.point_image)
                    self.points.add(point)
                    self.all_sprites.add(point)
                    self.add_node(j, i)
                elif element == 1:
                    brick = Brick(STARTMAPWIDTH + BRICKSWIDTH * j, BRICKSHEIGHT * i, self.brick_image)
                    self.bricks.add(brick)
                    self.all_sprites.add(brick)
                elif element == 2:
                    self.add_node(j, i)
                elif element == 3:
                    teleport = Teleport(STARTMAPWIDTH + BRICKSWIDTH * j, BRICKSHEIGHT * i, True)
                    self.left_teleport = teleport
                    self.teleports.add(teleport)
                    self.left_teleport_coords = (i, j)
                elif element == 4:
                    teleport = Teleport(STARTMAPWIDTH + BRICKSWIDTH * j, BRICKSHEIGHT * i, False)
                    self.right_teleport = teleport
                    self.teleports.add(teleport)
                elif element == 5:
                    pass
                else:
                    ghost = Ghost(GHOSTPOSITION[element - 6][0], GHOSTPOSITION[element - 6][1],
                                  self.ghosts_images[element - 6])
                    self.all_sprites.add(ghost)
                    self.ghosts.append(ghost)
                    self.ghosts_sprites.add(ghost)

    # checks if we are out of the game
    def check_events(self):
        message = self.interface.controls(self.pacman, self.menu)
        if message == 'switch':
            self.menu.switch()
        elif message == 'restart':
            self.restart()
        elif message == 'exit':
            self.running = False
        elif message == 1 or message == 2 or message == 3:
            if self.map_number != message - 1:
                self.map_number = message - 1
                self.restart()

    # moves entities to starting positions after pacman dies
    def reset_positions(self):
        self.timer.reset_time()
        self.pacman.rect.x = STARTPACMANPOSITION[0]
        self.pacman.rect.y = STARTPACMANPOSITION[1]
        for i in range(len(self.ghosts)):
            self.ghosts[i].rect.x = GHOSTPOSITION[i][0]
            self.ghosts[i].rect.y = GHOSTPOSITION[i][1]
            self.ghosts[i].deactivate()
            self.ghosts[i].path = []

    # checks that entities don't go through walls
    def check_collisions(self, obj):
        objects = pygame.sprite.spritecollide(obj, self.bricks, False)
        for element in objects:
            if obj.direction == "horizontal":
                if element.rect.x <= obj.rect.x:
                    obj.rect.x = element.rect.right
                else:
                    obj.rect.right = element.rect.left
                if len(objects) < 2 and self.pacman == obj:
                    self.grid_alignment("horizontal")
            elif obj.direction == "vertical":
                if element.rect.y <= obj.rect.y:
                    obj.rect.y = element.rect.bottom
                else:
                    obj.rect.bottom = element.rect.top
                if len(objects) < 2 and self.pacman == obj:
                    self.grid_alignment("vertical")

    # align pacman
    def grid_alignment(self, direction):
        if direction == "horizontal":
            if self.pacman.rect.centery - (
                    (self.pacman.rect.centery // BRICKSHEIGHT) * BRICKSHEIGHT + (
                    BRICKSHEIGHT // 2)) > self.pacman.speed:
                self.pacman.rect.centery -= self.pacman.speed
            elif ((self.pacman.rect.centery // BRICKSHEIGHT) * BRICKSHEIGHT + (
                    BRICKSHEIGHT // 2)) - self.pacman.rect.centery > self.pacman.speed:
                self.pacman.rect.centery += self.pacman.speed
        else:
            if self.pacman.rect.centerx - (
                    (self.pacman.rect.centerx // BRICKSWIDTH) * BRICKSWIDTH + (BRICKSWIDTH // 2)) > self.pacman.speed:
                self.pacman.rect.centerx -= self.pacman.speed

            elif ((self.pacman.rect.centerx // BRICKSWIDTH) * BRICKSWIDTH + (
                    BRICKSWIDTH // 2)) - self.pacman.rect.centerx > self.pacman.speed:
                self.pacman.rect.centerx += self.pacman.speed

    # checks if entity entered the teleport
    def check_teleports(self, obj):
        objects = pygame.sprite.spritecollide(obj, self.teleports, False)
        for x in objects:
            if x.rect.center == self.left_teleport.rect.center:
                obj.rect.right = self.right_teleport.rect.left
            else:
                obj.rect.left = self.left_teleport.rect.right

    # moves and activates ghosts
    def ghost_movement(self):
        for x in range(4):
            if self.timer.get_time() > 5 + x * 20 and not self.ghosts[x].is_active:
                self.ghosts[x].activate()
                self.ghosts[x].rect.x = STARTGHOSTPOSITION[0]
                self.ghosts[x].rect.y = STARTGHOSTPOSITION[1]
        index = 0
        for ghost in self.ghosts:
            if ghost.is_active:
                if self.timer.time % 10 == 0:
                    ghost.change_path(self.pacman_position[index][0], self.pacman_position[index][1], self.graph,
                                      self.vertices)
                    if index + 1 < len(self.pacman_position):
                        index += 1
                ghost.go_to_pacman()

    # finds node in graph where pacman is
    def check_pacman_position(self):
        objects = pygame.sprite.spritecollide(self.pacman, self.vertices, False)
        self.pacman_position = []
        for obj in objects:
            self.pacman_position.append((obj.rect.x, obj.rect.y))

    # checks collisions of ghosts sprites
    def check_ghost_collisions(self):
        for i in range(len(self.ghosts) - 1):
            for j in range(i + 1, len(self.ghosts)):
                if self.ghosts[i].is_active and self.ghosts[j].is_active \
                        and pygame.sprite.collide_rect(self.ghosts[i], self.ghosts[j]) and not self.ghosts[j].collision:
                    self.ghosts[j].collision = True
                    self.ghosts[j].change_direction()

    # checks if pacman earned all points
    def check_win(self):
        if self.pacman.score == POINTSNUMBER[self.map_number]:
            self.stop = True
            self.win = True

    # checks if pacman lost all his lives
    def check_loss(self):
        if self.pacman.lives == 0:
            self.stop = True
            self.loss = True

    # the main game loop, updates self.framerate once per second
    def run(self):
        while self.running:
            self.check_win()
            self.check_loss()
            self.check_events()
            if self.menu.state == 'running' and not self.stop:
                self.clock.tick(self.frame_rate)
                self.timer.tick()
                self.check_teleports(self.pacman)
                for ghost in self.ghosts:
                    self.check_teleports(ghost)
                self.all_sprites.update()
                self.check_collisions(self.pacman)
                self.check_pacman_position()
                self.ghost_movement()
                for ghost in self.ghosts:
                    self.check_collisions(ghost)
                self.check_ghost_collisions()
                points_not_eaten = pygame.sprite.spritecollide(self.pacman, self.points, True)
                if len(points_not_eaten) > 0:
                    self.pacman.add_point()
                hits = pygame.sprite.spritecollide(self.pacman, self.ghosts_sprites, False)
                if hits:
                    self.pacman.lives -= 1
                    if self.pacman.lives != 0:
                        self.reset_positions()
            self.interface.update(self.all_sprites, self.menu.get_active_buttons())
            self.interface.draw_text(str(self.pacman.score) + " Points", TEXTPOINTSCOORDS[0], TEXTPOINTSCOORDS[1])
            self.interface.draw_text("Time: " + str(self.timer.get_time()), TIMERPOSITION[0], TIMERPOSITION[1])
            self.interface.draw_text(str(self.pacman.lives) + " Lives", TEXTLIVESCOORDS[0], TEXTLIVESCOORDS[1])
            if self.menu.state != 'running':
                self.interface.draw_text('MENU', TEXTMENUPOSITION[0], TEXTMENUPOSITION[1])
            if self.menu.state == 'menu':
                self.interface.draw_text("play", BUTTONPOSITION[0][0] + 100, BUTTONPOSITION[0][1] + 40)
                self.interface.draw_text('restart', BUTTONPOSITION[1][0] + 100, BUTTONPOSITION[1][1] + 40)
                self.interface.draw_text('maps', BUTTONPOSITION[2][0] + 100, BUTTONPOSITION[2][1] + 40)
                self.interface.draw_text('exit', BUTTONPOSITION[3][0] + 100, BUTTONPOSITION[3][1] + 40)
            if self.menu.state == 'maps':
                self.interface.draw_text("return", BUTTONPOSITION[0][0] + 100, BUTTONPOSITION[0][1] + 40)
                self.interface.draw_text('map 1', BUTTONPOSITION[1][0] + 100, BUTTONPOSITION[1][1] + 40)
                self.interface.draw_text('map 2', BUTTONPOSITION[2][0] + 100, BUTTONPOSITION[2][1] + 40)
                self.interface.draw_text('map 3', BUTTONPOSITION[3][0] + 100, BUTTONPOSITION[3][1] + 40)
            if self.win:
                self.interface.draw_text("YOU WON!!!", WINORLOSSTEXTPOSITION[0], WINORLOSSTEXTPOSITION[1])
            if self.loss:
                self.interface.draw_text("YOU LOST:(", WINORLOSSTEXTPOSITION[0], WINORLOSSTEXTPOSITION[1])
            if self.stop:
                self.interface.draw_text("PRESS ESCAPE TO OPEN MENU", ESCAPEPOSITION[0], ESCAPEPOSITION[1])
            self.interface.end_update()


if __name__ == '__main__':
    PacmanGame().run()
