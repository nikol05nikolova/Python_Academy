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
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
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
                    if event.key == pygame.K_w:
                        self.player.jump()
            self.screen.fill(BACKGROUND_COLOR)
            self.player.update()
            self.player.keep_inside_screen()
            for platform in self.platforms:
                self.player.handle_collision(platform)
                platform.draw(self.screen)
            self.player.draw(self.screen)  
            pygame.display.update()
            self.clock.tick(60)