import pygame
from constants import *


class Player:
    def __init__(self, x, y, width, height, color, left_key, right_key, jump_key):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.x = x
        self.velocity_x = 0
        self.velocity_y = 0
        self.start_x = x
        self.start_y = y
        self.is_on_ground = False
        self.previous_rect = self.rect.copy()
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x = self.start_x
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def keep_inside_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity_x = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.reset()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.previous_rect = self.rect.copy()
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.velocity_x -= PLAYER_ACCELERATION
        if keys[self.right_key]:
            self.velocity_x += PLAYER_ACCELERATION
        if self.velocity_x > PLAYER_MAX_SPEED:
            self.velocity_x = PLAYER_MAX_SPEED
        if self.velocity_x < -PLAYER_MAX_SPEED:
            self.velocity_x = -PLAYER_MAX_SPEED
        self.x += self.velocity_x
        self.rect.x = int(self.x)
        self.velocity_x *= FRICTION
        if -0.1 < self.velocity_x < 0.1:
            self.velocity_x = 0

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def jump(self):
        if self.is_on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.is_on_ground = False

    def handle_collision(self, platform):
        if self.rect.colliderect(platform.rect):
            if self.previous_rect.right <= platform.rect.left:
                self.rect.right = platform.rect.left
                self.velocity_x = 0
            elif self.previous_rect.left >= platform.rect.right:
                self.rect.left = platform.rect.right
                self.velocity_x = 0
            elif self.previous_rect.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_on_ground = True
            elif self.previous_rect.top >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
