import pygame
from constants import *


class Player:
    def __init__(self, x, y, width, height, color, image_path, left_key, right_key, jump_key):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.start_x = x
        self.start_y = y
        self.is_on_ground = False
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key
        self.image_right = pygame.image.load(image_path).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (width, height))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.facing_right = True

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.velocity_x -= PLAYER_ACCELERATION
            self.facing_right = False
        if keys[self.right_key]:
            self.velocity_x += PLAYER_ACCELERATION
            self.facing_right = True
        if self.velocity_x > PLAYER_MAX_SPEED:
            self.velocity_x = PLAYER_MAX_SPEED
        if self.velocity_x < -PLAYER_MAX_SPEED:
            self.velocity_x = -PLAYER_MAX_SPEED

    def apply_gravity(self):
        self.velocity_y += GRAVITY

    def apply_friction(self):
        self.velocity_x *= FRICTION
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

    def move_horizontal(self, platforms, doors, computers):
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
        for door in doors:
            if not door.open and self.rect.colliderect(door.rect):
                if self.velocity_x > 0:
                    self.rect.right = door.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = door.rect.right
                self.x = self.rect.x
                self.velocity_x = 0
        for computer in computers:
            if self.rect.colliderect(computer.rect):
                if self.velocity_x > 0:
                    computer.push(self.velocity_x)
                    self.rect.right = computer.rect.left
                elif self.velocity_x < 0:
                    computer.push(self.velocity_x)
                    self.rect.left = computer.rect.right
                self.x = self.rect.x

    def move_vertical(self, platforms):
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

    def keep_inside_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
            self.velocity_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.x = self.rect.x
            self.velocity_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.y
            self.velocity_y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.reset()

    def update(self, platforms, doors, computers):
        self.handle_input()
        self.move_horizontal(platforms, doors, computers)
        self.apply_gravity()
        self.move_vertical(platforms)
        self.apply_friction()
        self.keep_inside_screen()

    def jump(self):
        if self.is_on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.is_on_ground = False

    def draw(self, screen):
        image = self.image_right if self.facing_right else self.image_left
        screen.blit(image, self.rect)
