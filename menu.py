import sys
import pygame
from constants import *


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 72)
        self.prompt_font = pygame.font.Font(None, 32)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return
            self.screen.fill(BACKGROUND_COLOR)
            title_surface = self.title_font.render(WINDOW_TITLE, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(title_surface, title_rect)
            prompt_surface = self.prompt_font.render("Press ENTER or SPACE to play", True, (200, 200, 200))
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(prompt_surface, prompt_rect)
            pygame.display.update()
            self.clock.tick(60)
