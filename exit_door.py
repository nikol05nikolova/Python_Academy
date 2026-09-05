import pygame


class ExitDoor:
    def __init__(self, x, y, width, height, image_path, player_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.player_number = player_number
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
