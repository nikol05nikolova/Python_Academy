import pygame


class Button:
    def __init__(self, x, y, width, height, color, player_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.player_number = player_number
        self.pressed = False

    def update(self, player_1, player_2):
        self.pressed = False

        if self.player_number == 1:
            if self.rect.colliderect(player_1.rect):
                self.pressed = True

        elif self.player_number == 2:
            if self.rect.colliderect(player_2.rect):
                self.pressed = True

    def draw(self, screen):
        if self.pressed:
            pygame.draw.rect(
                screen,
                self.color,
                (self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height - 5)
            )
        else:
            pygame.draw.rect(
                screen,
                self.color,
                self.rect
            )