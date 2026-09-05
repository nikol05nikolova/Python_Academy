import unittest
from unittest.mock import Mock, patch
import pygame
from constants import (
    BLUE_PUDDLE_COLOR,
    PLAYER_1_COLOR,
    PLAYER_2_COLOR,
    PLATFORM_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    YELLOW_PUDDLE_COLOR,
)
from game import Game
from game_platform import Platform
from puddle import Puddle
from snickers import Snickers


class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def create_game(self):
        game = Game.__new__(Game)
        game.player_1 = Mock()
        game.player_1.rect = pygame.Rect(100, 100, 50, 50)
        game.player_1.x = 100
        game.player_1.velocity_x = 0
        game.player_2 = Mock()
        game.player_2.rect = pygame.Rect(200, 100, 50, 50)
        game.player_2.x = 200
        game.player_2.velocity_x = 0
        game.snickers = []
        game.puddles = []
        game.doors = []
        game.exit_doors = []
        game.computers = []
        game.buttons = []
        game.platforms = []
        game.collected_snickers = 0
        game.level_complete = False
        return game

    def test_reset_level_resets_players(self):
        game = self.create_game()
        snickers = Mock()
        computer = Mock()
        game.snickers = [snickers]
        game.computers = [computer]
        game.collected_snickers = 5
        game.level_complete = True
        game.reset_level()
        game.player_1.reset.assert_called_once()
        game.player_2.reset.assert_called_once()
        snickers.reset.assert_called_once()
        computer.reset.assert_called_once()
        self.assertEqual(game.collected_snickers, 0)
        self.assertFalse(game.level_complete)

    def test_blue_player_can_enter_blue_puddle(self):
        game = self.create_game()
        puddle = Puddle(
            100,
            100,
            100,
            25,
            BLUE_PUDDLE_COLOR,
            "data/images/puddle_blue.png",
            "blue",
        )
        game.puddles = [puddle]
        with patch.object(game, "reset_level") as reset:
            game.check_puddles()
        reset.assert_not_called()

    def test_blue_player_dies_in_yellow_puddle(self):
        game = self.create_game()
        puddle = Puddle(
            100,
            100,
            100,
            25,
            YELLOW_PUDDLE_COLOR,
            "data/images/puddle_yellow.png",
            "yellow",
        )
        game.puddles = [puddle]
        with patch.object(game, "reset_level") as reset:
            game.check_puddles()
        reset.assert_called_once()

    def test_yellow_player_can_enter_yellow_puddle(self):
        game = self.create_game()
        game.player_2.rect = pygame.Rect(200, 100, 50, 50)
        puddle = Puddle(
            200,
            100,
            100,
            25,
            YELLOW_PUDDLE_COLOR,
            "data/images/puddle_yellow.png",
            "yellow",
        )
        game.puddles = [puddle]
        with patch.object(game, "reset_level") as reset:
            game.check_puddles()
        reset.assert_not_called()

    def test_yellow_player_dies_in_blue_puddle(self):
        game = self.create_game()
        game.player_2.rect = pygame.Rect(200, 100, 50, 50)
        puddle = Puddle(
            200,
            100,
            100,
            25,
            BLUE_PUDDLE_COLOR,
            "data/images/puddle_blue.png",
            "blue",
        )
        game.puddles = [puddle]
        with patch.object(game, "reset_level") as reset:
            game.check_puddles()
        reset.assert_called_once()

    def test_blue_player_dies_in_green_puddle(self):
        game = self.create_game()
        puddle = Puddle(
            100,
            100,
            100,
            25,
            (0, 255, 0),
            "data/images/puddle_green.png",
            "green",
        )
        game.puddles = [puddle]
        with patch.object(game, "reset_level") as reset:
            game.check_puddles()
        reset.assert_called_once()

    def test_level_is_complete_when_both_players_reach_exit(self):
        game = self.create_game()
        blue_exit = Mock()
        blue_exit.player_number = 1
        blue_exit.rect = pygame.Rect(100, 100, 50, 50)
        yellow_exit = Mock()
        yellow_exit.player_number = 2
        yellow_exit.rect = pygame.Rect(200, 100, 50, 50)
        game.exit_doors = [blue_exit, yellow_exit]
        game.check_exit_doors()
        self.assertTrue(game.level_complete)

    def test_level_is_not_complete_when_only_player_one_reaches_exit(self):
        game = self.create_game()
        blue_exit = Mock()
        blue_exit.player_number = 1
        blue_exit.rect = pygame.Rect(100, 100, 50, 50)
        yellow_exit = Mock()
        yellow_exit.player_number = 2
        yellow_exit.rect = pygame.Rect(500, 500, 50, 50)
        game.exit_doors = [blue_exit, yellow_exit]
        game.check_exit_doors()
        self.assertFalse(game.level_complete)

    def test_level_is_not_complete_when_only_player_two_reaches_exit(self):
        game = self.create_game()
        blue_exit = Mock()
        blue_exit.player_number = 1
        blue_exit.rect = pygame.Rect(500, 500, 50, 50)
        yellow_exit = Mock()
        yellow_exit.player_number = 2
        yellow_exit.rect = pygame.Rect(200, 100, 50, 50)
        game.exit_doors = [blue_exit, yellow_exit]
        game.check_exit_doors()
        self.assertFalse(game.level_complete)

    def test_closed_door_blocks_player_from_left(self):
        game = self.create_game()
        door = Mock()
        door.open = False
        door.rect = pygame.Rect(120, 100, 30, 100)
        game.player_1.rect = pygame.Rect(100, 110, 50, 50)
        game.player_1.x = 100
        game.player_1.velocity_x = 5
        game.doors = [door]
        game.handle_door_collisions()
        self.assertEqual(game.player_1.rect.right, door.rect.left)
        self.assertEqual(game.player_1.velocity_x, 0)

    def test_closed_door_blocks_player_from_right(self):
        game = self.create_game()
        door = Mock()
        door.open = False
        door.rect = pygame.Rect(100, 100, 30, 100)
        game.player_1.rect = pygame.Rect(110, 110, 50, 50)
        game.player_1.x = 110
        game.player_1.velocity_x = -5
        game.doors = [door]
        game.handle_door_collisions()
        self.assertEqual(game.player_1.rect.left, door.rect.right)
        self.assertEqual(game.player_1.velocity_x, 0)

    def test_open_door_does_not_block_player(self):
        game = self.create_game()
        door = Mock()
        door.open = True
        door.rect = pygame.Rect(120, 100, 30, 100)
        game.player_1.rect = pygame.Rect(100, 110, 50, 50)
        game.player_1.x = 100
        game.player_1.velocity_x = 5
        game.doors = [door]
        game.handle_door_collisions()
        self.assertEqual(game.player_1.rect.x, 100)
        self.assertEqual(game.player_1.velocity_x, 5)

    def test_player_one_collects_own_snickers(self):
        game = self.create_game()
        snickers = Snickers(
            100,
            100,
            50,
            30,
            "data/images/snickers_blue.png",
            1,
        )
        game.snickers = [snickers]
        game.player_1.update = Mock()
        game.player_2.update = Mock()
        game.update_world()
        self.assertTrue(snickers.collected)
        self.assertEqual(game.collected_snickers, 1)

    def test_player_two_collects_own_snickers(self):
        game = self.create_game()
        snickers = Snickers(
            200,
            100,
            50,
            30,
            "data/images/snickers_yellow.png",
            2,
        )
        game.snickers = [snickers]
        game.player_1.update = Mock()
        game.player_2.update = Mock()
        game.update_world()
        self.assertTrue(snickers.collected)
        self.assertEqual(game.collected_snickers, 1)

    def test_player_one_cannot_collect_player_two_snickers(self):
        game = self.create_game()
        snickers = Snickers(
            100,
            100,
            50,
            30,
            "data/images/snickers_yellow.png",
            2,
        )
        game.snickers = [snickers]
        game.player_1.update = Mock()
        game.player_2.update = Mock()
        game.update_world()
        self.assertFalse(snickers.collected)
        self.assertEqual(game.collected_snickers, 0)

    def test_player_two_cannot_collect_player_one_snickers(self):
        game = self.create_game()
        snickers = Snickers(
            200,
            100,
            50,
            30,
            "data/images/snickers_blue.png",
            1,
        )
        game.snickers = [snickers]
        game.player_1.update = Mock()
        game.player_2.update = Mock()
        game.update_world()
        self.assertFalse(snickers.collected)
        self.assertEqual(game.collected_snickers, 0)

    def test_collected_snickers_are_not_collected_again(self):
        game = self.create_game()
        snickers = Snickers(
            100,
            100,
            50,
            30,
            "data/images/snickers_blue.png",
            1,
        )
        snickers.collected = True
        game.snickers = [snickers]
        game.player_1.update = Mock()
        game.player_2.update = Mock()
        game.update_world()
        self.assertTrue(snickers.collected)
        self.assertEqual(game.collected_snickers, 0)

    def test_build_pause_entries_creates_two_entries(self):
        game = self.create_game()
        game.pause_entries = []
        game.build_pause_entries()
        self.assertEqual(len(game.pause_entries), 2)
        self.assertEqual(game.pause_entries[0][1], "Reset Level")
        self.assertEqual(
            game.pause_entries[1][1],
            "Return to Main Menu",
        )

    def test_build_pause_entries_creates_correct_button_size(self):
        game = self.create_game()
        game.pause_entries = []
        game.build_pause_entries()
        for rect, _ in game.pause_entries:
            self.assertEqual(rect.width, 320)
            self.assertEqual(rect.height, 44)


if __name__ == "__main__":
    unittest.main()