import unittest
from unittest.mock import patch
import pygame
from player import Player
from game_platform import Platform
from constants import PLATFORM_COLOR


class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def create_player(self):
        image = pygame.Surface((50, 50))
        with patch("pygame.image.load") as mock_load:
            mock_load.return_value.convert_alpha.return_value = image
            return Player(
                100,
                100,
                50,
                50,
                (50, 120, 255),
                "snake_blue.png",
                pygame.K_a,
                pygame.K_d,
                pygame.K_w
            )

    def test_player_starts_at_given_position(self):
        player = self.create_player()
        self.assertEqual(player.rect.topleft, (100, 100))

    def test_player_reset_returns_to_start_position(self):
        player = self.create_player()
        player.rect.x = 500
        player.rect.y = 500
        player.velocity_x = 5
        player.velocity_y = 10
        player.reset()
        self.assertEqual(player.rect.topleft, (100, 100))
        self.assertEqual(player.velocity_x, 0)
        self.assertEqual(player.velocity_y, 0)

    def test_player_jump_changes_vertical_velocity(self):
        player = self.create_player()
        player.is_on_ground = True
        player.jump()
        self.assertEqual(player.velocity_y, -15)
        self.assertFalse(player.is_on_ground)

    def test_player_cannot_jump_in_air(self):
        player = self.create_player()
        player.is_on_ground = False
        player.velocity_y = 5
        player.jump()
        self.assertEqual(player.velocity_y, 5)

    def test_gravity_increases_vertical_velocity(self):
        player = self.create_player()
        player.velocity_y = 0
        player.apply_gravity()
        self.assertEqual(player.velocity_y, 0.8)

    def test_friction_reduces_horizontal_velocity(self):
        player = self.create_player()
        player.velocity_x = 5
        player.apply_friction()
        self.assertEqual(player.velocity_x, 4)

    def test_player_lands_on_platform(self):
        player = self.create_player()
        platform = Platform(100, 150, 200, 20, PLATFORM_COLOR)
        player.velocity_y = 10
        player.move_vertical([platform], [])
        self.assertTrue(player.is_on_ground)
        self.assertEqual(player.rect.bottom, platform.rect.top)
        self.assertEqual(player.velocity_y, 0)

    def test_player_stops_at_left_screen_edge(self):
        player = self.create_player()
        player.rect.x = -10
        player.x = -10
        player.velocity_x = -5
        player.keep_inside_screen()
        self.assertEqual(player.rect.left, 0)
        self.assertEqual(player.velocity_x, 0)

    def test_player_stops_at_right_screen_edge(self):
        player = self.create_player()
        player.rect.right = 910
        player.x = 860
        player.velocity_x = 5
        player.keep_inside_screen()
        self.assertEqual(player.rect.right, 900)
        self.assertEqual(player.velocity_x, 0)


if __name__ == "__main__":
    unittest.main()