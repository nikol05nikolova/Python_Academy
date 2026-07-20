import pygame
from constants import *

class Player:

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity_y = 0
        self.gravity = GRAVITY
        self.jump_strength = JUMP_STRENGTH
        self.is_on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
    
    def jump(self):
        if self.is_on_ground:
            self.velocity_y = self.jump_strength

    def handle_collision(self, platform):
        if self.rect.colliderect(platform.rect):
            if self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_on_ground = True