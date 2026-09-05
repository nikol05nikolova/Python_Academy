import unittest
import pygame
from game_platform import Platform


class TestPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_platform_creates_correct_rect(self):
        platform = Platform(100, 200, 300, 20, (100, 100, 100))
        self.assertEqual(platform.rect.x, 100)
        self.assertEqual(platform.rect.y, 200)
        self.assertEqual(platform.rect.width, 300)
        self.assertEqual(platform.rect.height, 20)

    def test_platform_stores_color(self):
        color = (100, 100, 100)
        platform = Platform(0, 0, 100, 20, color)
        self.assertEqual(platform.color, color)


if __name__ == "__main__":
    unittest.main()