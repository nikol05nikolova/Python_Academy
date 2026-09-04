import pygame
from constants import *


class Computer:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.x = float(x)
        self.y = float(y)
        self.start_x = x
        self.start_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def apply_gravity(self):
        self.velocity_y += GRAVITY

    def apply_friction(self):
        self.velocity_x *= FRICTION
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

    def can_move_horizontal(self, new_rect, platforms, computers, doors):
        for platform in platforms:
            if new_rect.colliderect(platform.rect):
                return False
        for door in doors:
            if not door.open and new_rect.colliderect(door.rect):
                return False
        for computer in computers:
            if computer is not self and new_rect.colliderect(computer.rect):
                return False
        if new_rect.left < 0 or new_rect.right > SCREEN_WIDTH:
            return False
        return True

    def move_horizontal(self, platforms, computers, doors):
        if self.velocity_x == 0:
            return
        new_rect = self.rect.copy()
        new_rect.x += round(self.velocity_x)
        if self.can_move_horizontal(new_rect, platforms, computers, doors):
            self.x += self.velocity_x
            self.rect.x = round(self.x)
        else:
            self.velocity_x = 0

    def move_vertical(self, platforms, computers, doors):
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
        for door in doors:
            if door.open:
                continue
            if self.rect.colliderect(door.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = door.rect.top
                    self.is_on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = door.rect.bottom
                self.y = self.rect.y
                self.velocity_y = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.y
            self.velocity_y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y = self.rect.y
            self.velocity_y = 0
            self.is_on_ground = True

    def push(self, velocity):
        self.velocity_x = velocity

    def update(self, platforms, computers, doors):
        self.move_horizontal(platforms, computers, doors)
        self.apply_gravity()
        self.move_vertical(platforms, computers, doors)
        self.apply_friction()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)