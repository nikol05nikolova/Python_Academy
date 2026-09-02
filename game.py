import sys
import pygame
from constants import *
from player import Player
from game_platform import Platform


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player_1 = Player(PLAYER_1_START_X, PLAYER_1_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_1_COLOR, pygame.K_a, pygame.K_d, pygame.K_w)
        self.player_2 = Player(PLAYER_2_START_X, PLAYER_2_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_2_COLOR, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
        self.platforms = [
                            Platform(0, 650, 900, 50, PLATFORM_COLOR),

                            Platform(120, 570, 180, 20, PLATFORM_COLOR),

                            Platform(420, 460, 180, 20, PLATFORM_COLOR),

                            Platform(180, 340, 160, 20, PLATFORM_COLOR),

                            Platform(520, 250, 180, 20, PLATFORM_COLOR)
                        ]
        
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
            self.player_1.update()
            self.player_2.update()
            self.player_1.keep_inside_screen()
            self.player_2.keep_inside_screen()
            for platform in self.platforms:
                self.player_1.handle_collision(platform)
                self.player_2.handle_collision(platform)
                platform.draw(self.screen)
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)