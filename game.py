import sys
import pygame
from constants import *
from player import Player
from game_platform import Platform
from snickers import Snickers
from puddle import Puddle
from button import Button
from door import Door


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
            "data/images/snake_blue.png",
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
            "data/images/snake_yellow.png",
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
            Snickers(200, 527, SNICKERS_WIDTH, SNICKERS_HEIGHT,  "data/images/snickers_blue.png", 1),
            Snickers(460, 417, SNICKERS_WIDTH, SNICKERS_HEIGHT, "data/images/snickers_yellow.png", 2),
            Snickers(230, 297, SNICKERS_WIDTH, SNICKERS_HEIGHT, "data/images/snickers_blue.png", 1),
            Snickers(580, 207, SNICKERS_WIDTH, SNICKERS_HEIGHT, "data/images/snickers_yellow.png", 2),
        ]
        self.collected_snickers = 0

        self.puddles = [
            Puddle(
                350,
                640,
                90,
                PUDDLE_HEIGHT,
                BLUE_PUDDLE_COLOR,
                "data/images/puddle_blue.png",
                "blue",
            ),
            Puddle(
                530,
                640,
                90,
                PUDDLE_HEIGHT,
                YELLOW_PUDDLE_COLOR,
                "data/images/puddle_yellow.png",
                "yellow",
            ),
            Puddle(
                750,
                640,
                100,
                PUDDLE_HEIGHT,
                GREEN_PUDDLE_COLOR,
                "data/images/puddle_green.png",
                "green",
            ),
        ]

        self.buttons = [
            Button(
                250,
                330,
                50,
                20,
                BLUE_PUDDLE_COLOR,
                1,
            ),
            Button(
                600,
                240,
                50,
                20,
                YELLOW_PUDDLE_COLOR,
                2,
            ),
        ]

        self.doors = [
            Door(
                500,
                590,
                30,
                60,
                PLATFORM_COLOR,
            ),
        ]

    def reset_level(self):
        self.player_1.reset()
        self.player_2.reset()
        for snickers in self.snickers:
            snickers.reset()
        self.collected_snickers = 0

    def check_puddles(self):
        for puddle in self.puddles:
            if self.player_1.rect.colliderect(puddle.rect):
                if puddle.puddle_type != "blue":
                    self.reset_level()
            if self.player_2.rect.colliderect(puddle.rect):
                if puddle.puddle_type != "yellow":
                    self.reset_level()

    def handle_door_collisions(self):
        players = [self.player_1, self.player_2]
        for door in self.doors:
            if door.open:
                continue
            for player in players:
                if not player.rect.colliderect(door.rect):
                    continue
                if player.rect.centerx < door.rect.centerx:
                    player.rect.right = door.rect.left
                else:
                    player.rect.left = door.rect.right
                player.x = player.rect.x
                player.velocity_x = 0

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
            self.player_1.update(self.platforms, self.doors)
            self.player_2.update(self.platforms, self.doors)
            self.check_puddles()
            for button in self.buttons:
                button.update(self.player_1, self.player_2)
            for door in self.doors:
                door.update(self.buttons[0])
            self.handle_door_collisions()
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
            for puddle in self.puddles:
                puddle.draw(self.screen)
            for button in self.buttons:
                button.draw(self.screen)
            for door in self.doors:
                door.draw(self.screen)
            for snickers in self.snickers:
                snickers.draw(self.screen)
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)
            self.draw_ui()
            pygame.display.update()
            self.clock.tick(60)
