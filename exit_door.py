import pygame


class ExitDoor:
    def __init__(self, x, y, width, height, color, player_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.player_number = player_number

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
