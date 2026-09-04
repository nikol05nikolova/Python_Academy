import pygame
from constants import *


class Computer:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY

    def apply_friction(self):
        self.velocity_x *= FRICTION
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

    def move_vertical(self, platforms, computers):
        self.is_on_ground = False
        self.y += self.velocity_y
        self.rect.y = round(self.y)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.is_on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                self.y = self.rect.y
                self.velocity_y = 0
        for computer in computers:
            if computer is self:
                continue
            if self.rect.colliderect(computer.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = computer.rect.top
                    self.is_on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = computer.rect.bottom
                self.y = self.rect.y
                self.velocity_y = 0

    def move_horizontal(self, platforms, computers):
        self.x += self.velocity_x
        self.rect.x = round(self.x)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                self.x = self.rect.x
                self.velocity_x = 0
        for computer in computers:
            if computer is self:
                continue
            if self.rect.colliderect(computer.rect):
                if self.velocity_x > 0:
                    self.rect.right = computer.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = computer.rect.right
                self.x = self.rect.x
                self.velocity_x = 0

    def update(self, platforms, computers):
        self.move_horizontal(platforms, computers)
        self.apply_gravity()
        self.move_vertical(platforms, computers)
        self.apply_friction()

    def push(self, velocity):
        self.velocity_x = velocity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)