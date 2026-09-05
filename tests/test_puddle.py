import unittest
from unittest.mock import patch
import pygame
from puddle import Puddle


class TestPuddle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_puddle_creates_correct_rect(self, mock_load):
        image = pygame.Surface((100, 25))
        mock_load.return_value.convert_alpha.return_value = image
        puddle = Puddle(
            100, 200, 150, 25,
            (50, 120, 255),
            "puddle_blue.png",
            "blue"
        )
        self.assertEqual(puddle.rect.x, 100)
        self.assertEqual(puddle.rect.y, 200)
        self.assertEqual(puddle.rect.width, 150)
        self.assertEqual(puddle.rect.height, 25)

    @patch("pygame.image.load")
    def test_puddle_stores_type(self, mock_load):
        image = pygame.Surface((100, 25))
        mock_load.return_value.convert_alpha.return_value = image
        puddle = Puddle(
            100, 200, 150, 25,
            (50, 120, 255),
            "puddle_blue.png",
            "blue"
        )
        self.assertEqual(puddle.puddle_type, "blue")


if __name__ == "__main__":
    unittest.main()