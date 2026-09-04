import pygame


class Door:
    def __init__(self, x, y, width, height, image_path, button):
        self.rect = pygame.Rect(x, y, width, height)
        self.button = button
        self.open = False
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (width, height)
        )

    def update(self, computers):
        self.open = self.button.pressed
        if not self.open:
            for computer in computers:
                if self.rect.colliderect(computer.rect):
                    self.open = True
                    break

    def draw(self, screen):
        if not self.open:
            screen.blit(self.image, self.rect)