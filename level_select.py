import sys
import pygame
from constants import *


class LevelSelect:
    def __init__(self, level_paths):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 56)
        self.item_font = pygame.font.Font(None, 40)
        self.level_paths = level_paths
        self.entries = []

    def build_entries(self):
        self.entries = []
        start_y = 220
        spacing = 60
        for index, path in enumerate(self.level_paths):
            label = f"Level {index + 1}"
            rect = pygame.Rect(0, 0, 300, 44)
            rect.center = (SCREEN_WIDTH // 2, start_y + index * spacing)
            self.entries.append((rect, path, label))

    def run(self):
        self.build_entries()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, path, _ in self.entries:
                        if rect.collidepoint(event.pos):
                            return path
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if index < len(self.entries):
                            return self.entries[index][1]
            self.screen.fill(BACKGROUND_COLOR)
            title_surface = self.title_font.render("Select a Level", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
            self.screen.blit(title_surface, title_rect)
            mouse_pos = pygame.mouse.get_pos()
            for rect, _, label in self.entries:
                hovered = rect.collidepoint(mouse_pos)
                color = (90, 90, 90) if hovered else (60, 60, 60)
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                text_surface = self.item_font.render(label, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)
            pygame.display.update()
            self.clock.tick(60)
