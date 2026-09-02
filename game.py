import sys
import pygame
from constants import *
from player import Player
from game_platform import Platform
from snickers import Snickers


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.player_1 = Player(
            PLAYER_1_START_X,
            PLAYER_1_START_Y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_1_COLOR,
            pygame.K_a,
            pygame.K_d,
            pygame.K_w,
        )
        self.player_2 = Player(
            PLAYER_2_START_X,
            PLAYER_2_START_Y,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_2_COLOR,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
        )
        self.platforms = [
            Platform(0, 650, 900, 50, PLATFORM_COLOR),
            Platform(120, 570, 180, 20, PLATFORM_COLOR),
            Platform(420, 460, 180, 20, PLATFORM_COLOR),
            Platform(180, 340, 160, 20, PLATFORM_COLOR),
            Platform(520, 250, 180, 20, PLATFORM_COLOR),
        ]

        self.snickers = [
            Snickers(200, 535, SNICKERS_WIDTH, SNICKERS_HEIGHT, SNICKERS_BLUE_COLOR, 1),
            Snickers(460, 425, SNICKERS_WIDTH, SNICKERS_HEIGHT, SNICKERS_YELLOW_COLOR, 2),
            Snickers(230, 305, SNICKERS_WIDTH, SNICKERS_HEIGHT, SNICKERS_BLUE_COLOR, 1),
            Snickers(580, 215, SNICKERS_WIDTH, SNICKERS_HEIGHT, SNICKERS_YELLOW_COLOR, 2),
        ]
        self.collected_snickers = 0

    def draw_ui(self):
        collected = self.collected_snickers
        total = len(self.snickers)

        text = self.font.render(
            f"Snickers: {collected} / {total}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (20, 20))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == self.player_1.jump_key:
                        self.player_1.jump()
                    if event.key == self.player_2.jump_key:
                        self.player_2.jump()
            self.screen.fill(BACKGROUND_COLOR)
            self.player_1.update(self.platforms)
            self.player_2.update(self.platforms)
            for snickers in self.snickers:
                if (
                    not snickers.collected
                    and self.player_1.rect.colliderect(snickers.rect)
                    and snickers.player_number == 1
                ):
                    snickers.collect()
                    self.collected_snickers += 1

                if (
                    not snickers.collected
                    and self.player_2.rect.colliderect(snickers.rect)
                    and snickers.player_number == 2
                ):
                    snickers.collect()
                    self.collected_snickers += 1
            for platform in self.platforms:
                platform.draw(self.screen)
            for snickers in self.snickers:
                snickers.draw(self.screen)
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)
            self.draw_ui()
            pygame.display.update()
            self.clock.tick(60)
