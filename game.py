import sys
import pygame
from constants import *
from player import Player
from level_loader import load_level


class Game:
    def __init__(self, level_path):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.pause_title_font = pygame.font.Font(None, 48)
        self.pause_item_font = pygame.font.Font(None, 36)
        self.complete_font = pygame.font.Font(None, 72)
        self.level_path = level_path
        self.paused = False
        self.level_complete = False
        self.pause_entries = []
        self.build_level()

    def build_level(self):
        level = load_level(self.level_path)
        self.player_1 = Player(
            level.player_1_start["x"],
            level.player_1_start["y"],
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_1_COLOR,
            "data/images/snake_blue.png",
            pygame.K_a,
            pygame.K_d,
            pygame.K_w,
        )
        self.player_2 = Player(
            level.player_2_start["x"],
            level.player_2_start["y"],
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_2_COLOR,
            "data/images/snake_yellow.png",
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
        )
        self.platforms = level.platforms
        self.snickers = level.snickers
        self.collected_snickers = 0
        self.puddles = level.puddles
        self.buttons = level.buttons
        self.doors = level.doors
        self.exit_doors = level.exit_doors
        self.computers = level.computers

    def reset_level(self):
        self.player_1.reset()
        self.player_2.reset()
        for snickers in self.snickers:
            snickers.reset()
        for computer in self.computers:
            computer.reset()
        self.collected_snickers = 0
        self.level_complete = False

    def check_puddles(self):
        for puddle in self.puddles:
            if self.player_1.rect.colliderect(puddle.rect):
                if puddle.puddle_type != "blue":
                    self.reset_level()
            if self.player_2.rect.colliderect(puddle.rect):
                if puddle.puddle_type != "yellow":
                    self.reset_level()

    def check_exit_doors(self):
        player_1_at_exit = False
        player_2_at_exit = False
        for exit_door in self.exit_doors:
            if exit_door.player_number == 1:
                if self.player_1.rect.colliderect(exit_door.rect):
                    player_1_at_exit = True
            elif exit_door.player_number == 2:
                if self.player_2.rect.colliderect(exit_door.rect):
                    player_2_at_exit = True
        if player_1_at_exit and player_2_at_exit:
            self.level_complete = True

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
            f"Snickers: {collected} / {total}", True, (255, 255, 255)
        )
        self.screen.blit(text, (20, 20))

    def build_pause_entries(self):
        self.pause_entries = []
        labels = ["Reset Level", "Return to Main Menu"]
        start_y = SCREEN_HEIGHT // 2 - 10
        spacing = 60
        for index, label in enumerate(labels):
            rect = pygame.Rect(0, 0, 320, 44)
            rect.center = (SCREEN_WIDTH // 2, start_y + index * spacing)
            self.pause_entries.append((rect, label))

    def draw_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        title_surface = self.pause_title_font.render("Paused", True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
        )
        self.screen.blit(title_surface, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        for rect, label in self.pause_entries:
            hovered = rect.collidepoint(mouse_pos)
            color = (90, 90, 90) if hovered else (60, 60, 60)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            text_surface = self.pause_item_font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def draw_level_complete(self):
        self.screen.fill(BACKGROUND_COLOR)
        title_surface = self.complete_font.render(
            "Level Complete!", True, (255, 255, 255)
        )
        title_rect = title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(title_surface, title_rect)
        snickers_surface = self.font.render(
            f"Snickers: {self.collected_snickers} / {len(self.snickers)}",
            True,
            (255, 255, 255),
        )
        snickers_rect = snickers_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        )
        self.screen.blit(snickers_surface, snickers_rect)
        continue_surface = self.font.render(
            "Press Enter or Space to continue", True, (255, 255, 255)
        )
        continue_rect = continue_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        )
        self.screen.blit(continue_surface, continue_rect)

    def run(self):
        self.build_pause_entries()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.level_complete:
                        self.paused = not self.paused
                    elif self.level_complete:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            return
                    elif not self.paused:
                        if event.key == self.player_1.jump_key:
                            self.player_1.jump()
                        if event.key == self.player_2.jump_key:
                            self.player_2.jump()
                if (
                    self.paused
                    and event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    for rect, label in self.pause_entries:
                        if rect.collidepoint(event.pos):
                            if label == "Reset Level":
                                self.reset_level()
                                self.paused = False
                            elif label == "Return to Main Menu":
                                return
            if not self.paused and not self.level_complete:
                self.update_world()
            if self.level_complete:
                self.draw_level_complete()
            else:
                self.draw_world()
                if self.paused:
                    self.draw_pause_overlay()
            pygame.display.update()
            self.clock.tick(60)

    def update_world(self):
        for computer in self.computers:
            computer.update(self.platforms, self.computers, self.doors)
        self.player_1.update(self.platforms, self.doors, self.computers)
        self.player_2.update(self.platforms, self.doors, self.computers)
        self.check_puddles()
        for button in self.buttons:
            button.update(self.player_1, self.player_2, self.computers)
        for door in self.doors:
            door.update(self.computers)
        self.handle_door_collisions()
        self.check_exit_doors()
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

    def draw_world(self):
        self.screen.fill(BACKGROUND_COLOR)
        for platform in self.platforms:
            platform.draw(self.screen)
        for puddle in self.puddles:
            puddle.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for door in self.doors:
            door.draw(self.screen)
        for exit_door in self.exit_doors:
            exit_door.draw(self.screen)
        for snickers in self.snickers:
            snickers.draw(self.screen)
        for computer in self.computers:
            computer.draw(self.screen)
        if not self.level_complete:
            self.player_1.draw(self.screen)
            self.player_2.draw(self.screen)
        self.draw_ui()
