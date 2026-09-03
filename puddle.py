import pygame


class Puddle:
    def __init__(self, x, y, width, height, color, puddle_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.puddle_type = puddle_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
