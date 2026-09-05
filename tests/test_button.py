import unittest
from unittest.mock import patch
import pygame
from button import Button


class TestButton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_button_starts_unpressed(self, mock_load):
        image = pygame.Surface((50, 20))
        mock_load.return_value.convert_alpha.return_value = image
        button = Button(
            100, 200, 50, 20, (240, 100, 170), "button.png", "button_pressed.png"
        )
        self.assertFalse(button.pressed)

    @patch("pygame.image.load")
    def test_button_is_pressed_by_player(self, mock_load):
        image = pygame.Surface((50, 20))
        mock_load.return_value.convert_alpha.return_value = image
        button = Button(
            100, 200, 50, 20, (240, 100, 170), "button.png", "button_pressed.png"
        )
        player_1 = pygame.sprite.Sprite()
        player_1.rect = pygame.Rect(100, 200, 50, 50)
        player_2 = pygame.sprite.Sprite()
        player_2.rect = pygame.Rect(500, 500, 50, 50)
        button.update(player_1, player_2, [])
        self.assertTrue(button.pressed)

    @patch("pygame.image.load")
    def test_button_is_pressed_by_computer(self, mock_load):
        image = pygame.Surface((50, 20))
        mock_load.return_value.convert_alpha.return_value = image
        button = Button(
            100, 200, 50, 20, (240, 100, 170), "button.png", "button_pressed.png"
        )
        player_1 = pygame.sprite.Sprite()
        player_1.rect = pygame.Rect(500, 500, 50, 50)
        player_2 = pygame.sprite.Sprite()
        player_2.rect = pygame.Rect(600, 500, 50, 50)
        computer = pygame.sprite.Sprite()
        computer.rect = pygame.Rect(100, 200, 50, 50)
        button.update(player_1, player_2, [computer])
        self.assertTrue(button.pressed)

    @patch("pygame.image.load")
    def test_button_is_not_pressed_without_collision(self, mock_load):
        image = pygame.Surface((50, 20))
        mock_load.return_value.convert_alpha.return_value = image
        button = Button(
            100, 200, 50, 20, (240, 100, 170), "button.png", "button_pressed.png"
        )
        player_1 = pygame.sprite.Sprite()
        player_1.rect = pygame.Rect(500, 500, 50, 50)
        player_2 = pygame.sprite.Sprite()
        player_2.rect = pygame.Rect(600, 500, 50, 50)
        button.update(player_1, player_2, [])
        self.assertFalse(button.pressed)


if __name__ == "__main__":
    unittest.main()
