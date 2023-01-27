import pygame
from config import TEXTSIZE, WHITE, BLACK


class Interface:
    def __init__(self, caption, width, height):
        pygame.init()
        self.time = 0
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.font_name = pygame.font.match_font('arial')

    # checks the keyboard
    def controls(self, pacman, menu):
        self.time += 1
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_w]:
            pacman.direction = "UP"
        elif key_state[pygame.K_a]:
            pacman.direction = "LEFT"
        elif key_state[pygame.K_s]:
            pacman.direction = "DOWN"
        elif key_state[pygame.K_d]:
            pacman.direction = "RIGHT"
        elif key_state[pygame.K_ESCAPE]:
            if self.time >= 30:
                self.time = 0
                return 'switch'
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                buttons = menu.get_active_buttons()
                if buttons is not None:
                    for i in range(len(buttons)):
                        if buttons[i].rect.collidepoint(mouse):
                            temp = menu.press_button(i)
                            if temp == "restart" or temp == 'exit':
                                return temp
                            if temp == 1 or temp == 2 or temp == 3:
                                return temp
        return 'nothing'

    # prints the passed text
    def draw_text(self, text, x, y):
        font = pygame.font.Font(self.font_name, TEXTSIZE)
        text_surface = font.render(str(text), True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    # draws all sprites
    def update(self, sprites, buttons):
        self.screen.fill(BLACK)
        sprites.draw(self.screen)
        buttons_sprites = pygame.sprite.Group()
        if buttons is not None:
            for button in buttons:
                buttons_sprites.add(button)
        buttons_sprites.draw(self.screen)

    def end_update(self):
        pygame.display.flip()
