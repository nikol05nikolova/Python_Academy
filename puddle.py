import pygame


class Puddle:
    def __init__(self, x, y, width, height, color, image_path, puddle_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.puddle_type = puddle_type
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
