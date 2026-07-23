import pygame
from constants import *

class Player:

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.x = x
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def reset(self):
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y
        self.x = PLAYER_START_X  
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x -= PLAYER_ACCELERATION
        if keys[pygame.K_d]:
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
            if self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_on_ground = True