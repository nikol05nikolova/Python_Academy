import unittest
from unittest.mock import patch
import pygame
from door import Door


class TestDoor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_door_starts_closed(self, mock_load):
        image = pygame.Surface((30, 100))
        mock_load.return_value.convert_alpha.return_value = image
        door = Door(
            100, 200, 30, 100,
            "door_pink.png",
            []
        )
        self.assertFalse(door.open)

    @patch("pygame.image.load")
    def test_door_opens_when_button_is_pressed(self, mock_load):
        image = pygame.Surface((30, 100))
        mock_load.return_value.convert_alpha.return_value = image
        button = unittest.mock.Mock()
        button.pressed = True
        door = Door(
            100, 200, 30, 100,
            "door_pink.png",
            [button]
        )
        door.update([])
        self.assertTrue(door.open)

    @patch("pygame.image.load")
    def test_door_stays_closed_when_button_is_not_pressed(self, mock_load):
        image = pygame.Surface((30, 100))
        mock_load.return_value.convert_alpha.return_value = image
        button = unittest.mock.Mock()
        button.pressed = False
        door = Door(
            100, 200, 30, 100,
            "door_pink.png",
            [button]
        )
        door.update([])
        self.assertFalse(door.open)

    @patch("pygame.image.load")
    def test_door_opens_when_computer_reaches_it(self, mock_load):
        image = pygame.Surface((30, 100))
        mock_load.return_value.convert_alpha.return_value = image
        door = Door(
            100, 200, 30, 100,
            "door_pink.png",
            []
        )
        computer = unittest.mock.Mock()
        computer.rect = pygame.Rect(100, 200, 50, 50)
        door.update([computer])
        self.assertTrue(door.open)


if __name__ == "__main__":
    unittest.main()