import pygame


class Door:
    def __init__(self, x, y, width, height, color, button):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.button = button
        self.open = False

    def update(self):
        self.open = self.button.pressed

    def draw(self, screen):
        if not self.open:
            pygame.draw.rect(screen, self.color, self.rect)