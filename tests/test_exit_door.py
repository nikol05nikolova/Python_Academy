import unittest
from unittest.mock import patch
import pygame
from exit_door import ExitDoor


class TestExitDoor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_exit_door_has_correct_player_number(self, mock_load):
        image = pygame.Surface((50, 75))
        mock_load.return_value.convert_alpha.return_value = image
        door = ExitDoor(
            200, 300, 50, 75,
            "exit_door_blue.png",
            1
        )
        self.assertEqual(door.player_number, 1)

    @patch("pygame.image.load")
    def test_exit_door_creates_correct_rect(self, mock_load):
        image = pygame.Surface((50, 75))
        mock_load.return_value.convert_alpha.return_value = image
        door = ExitDoor(
            200, 300, 50, 75,
            "exit_door_blue.png",
            1
        )
        self.assertEqual(door.rect, pygame.Rect(200, 300, 50, 75))


if __name__ == "__main__":
    unittest.main()