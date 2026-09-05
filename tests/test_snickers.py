import unittest
from unittest.mock import patch
import pygame
from snickers import Snickers


class TestSnickers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_snickers_starts_not_collected(self, mock_load):
        image = pygame.Surface((50, 30))
        mock_load.return_value.convert_alpha.return_value = image
        snickers = Snickers(100, 200, 50, 30, "snickers_blue.png", 1)
        self.assertFalse(snickers.collected)

    @patch("pygame.image.load")
    def test_collect_marks_snickers_as_collected(self, mock_load):
        image = pygame.Surface((50, 30))
        mock_load.return_value.convert_alpha.return_value = image
        snickers = Snickers(100, 200, 50, 30, "snickers_blue.png", 1)
        snickers.collect()
        self.assertTrue(snickers.collected)

    @patch("pygame.image.load")
    def test_reset_makes_snickers_available_again(self, mock_load):
        image = pygame.Surface((50, 30))
        mock_load.return_value.convert_alpha.return_value = image
        snickers = Snickers(100, 200, 50, 30, "snickers_blue.png", 1)
        snickers.collect()
        snickers.reset()
        self.assertFalse(snickers.collected)

    @patch("pygame.image.load")
    def test_snickers_has_correct_player_number(self, mock_load):
        image = pygame.Surface((50, 30))
        mock_load.return_value.convert_alpha.return_value = image
        snickers = Snickers(100, 200, 50, 30, "snickers_yellow.png", 2)
        self.assertEqual(snickers.player_number, 2)


if __name__ == "__main__":
    unittest.main()
