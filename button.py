import pygame


class Button:
    def __init__(self, x, y, width, height, color, image_path, pressed_image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.pressed = False
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.pressed_image = pygame.image.load(pressed_image_path).convert_alpha()
        self.pressed_image = pygame.transform.scale(self.pressed_image, (width, height))

    def update(self, player_1, player_2, computers):
        self.pressed = self.rect.colliderect(player_1.rect) or self.rect.colliderect(
            player_2.rect
        )
        for computer in computers:
            if self.rect.colliderect(computer.rect):
                self.pressed = True
                break

    def draw(self, screen):
        if self.pressed:
            image = pygame.transform.scale(self.pressed_image, self.rect.size)
        else:
            image = self.image
        screen.blit(image, self.rect)
