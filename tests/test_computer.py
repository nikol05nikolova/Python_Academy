import unittest
from unittest.mock import patch
import pygame
from computer import Computer


class TestComputer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_computer_starts_at_given_position(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        computer = Computer(
            100, 200, 50, 50,
            "computer.png"
        )
        self.assertEqual(computer.rect.topleft, (100, 200))

    @patch("pygame.image.load")
    def test_computer_reset_returns_to_start_position(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        computer = Computer(
            100, 200, 50, 50,
            "computer.png"
        )
        computer.rect.x = 400
        computer.rect.y = 500
        computer.reset()
        self.assertEqual(computer.rect.topleft, (100, 200))

    @patch("pygame.image.load")
    def test_computer_push_changes_velocity(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        computer = Computer(
            100, 200, 50, 50,
            "computer.png"
        )
        computer.push(5)
        self.assertEqual(computer.velocity_x, 5)

    @patch("pygame.image.load")
    def test_computer_can_move_inside_screen(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        computer = Computer(
            100, 200, 50, 50,
            "computer.png"
        )
        new_rect = computer.rect.copy()
        new_rect.x += 10
        self.assertTrue(
            computer.can_move_horizontal(
                new_rect,
                [],
                [computer],
                []
            )
        )


if __name__ == "__main__":
    unittest.main()