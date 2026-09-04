import pygame


class Door:
    def __init__(self, x, y, width, height, color, button):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.button = button
        self.open = False

    def update(self, computers):
        self.open = self.button.pressed
        if not self.open:
            for computer in computers:
                if self.rect.colliderect(computer.rect):
                    self.open = True
                    break

    def draw(self, screen):
        if not self.open:
            pygame.draw.rect(screen, self.color, self.rect)