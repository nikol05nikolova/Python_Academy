import pygame


class Button:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.pressed = False

    def update(self, player_1, player_2, computers):
        self.pressed = (
            self.rect.colliderect(player_1.rect)
            or self.rect.colliderect(player_2.rect)
        )
        for computer in computers:
            if self.rect.colliderect(computer.rect):
                self.pressed = True
                break

    def draw(self, screen):
        if self.pressed:
            pygame.draw.rect(
                screen,
                self.color,
                (self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height - 5)
            )
        else:
            pygame.draw.rect(screen, self.color, self.rect)