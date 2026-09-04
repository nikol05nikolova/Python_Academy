import pygame


class Snickers:
    def __init__(self, x, y, width, height, image_path, player_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.player_number = player_number
        self.collected = False
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def collect(self):
        self.collected = True

    def reset(self):
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)
