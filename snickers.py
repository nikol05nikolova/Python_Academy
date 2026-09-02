import pygame


class Snickers:
    def __init__(self, x, y, width, height, color, player_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.player_number = player_number
        self.collected = False

    def collect(self):
        self.collected = True

    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)