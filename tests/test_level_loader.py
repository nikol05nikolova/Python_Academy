import unittest
import json
import tempfile
import os
from unittest.mock import patch
import pygame
from level_loader import load_level, list_levels


class TestLevelLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    @patch("pygame.image.load")
    def test_load_level_reads_player_start_positions(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        data = {
            "player_1_start": {"x": 100, "y": 200},
            "player_2_start": {"x": 300, "y": 200},
            "platforms": [],
            "snickers": [],
            "puddles": [],
            "buttons": [],
            "doors": [],
            "exit_doors": [],
            "computers": [],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as file:
            json.dump(data, file)
            path = file.name
        try:
            level = load_level(path)

            self.assertEqual(level.player_1_start, {"x": 100, "y": 200})
            self.assertEqual(level.player_2_start, {"x": 300, "y": 200})
        finally:
            os.remove(path)

    @patch("pygame.image.load")
    def test_load_level_creates_platforms(self, mock_load):
        image = pygame.Surface((50, 50))
        mock_load.return_value.convert_alpha.return_value = image
        data = {
            "player_1_start": {"x": 0, "y": 0},
            "player_2_start": {"x": 50, "y": 0},
            "platforms": [{"x": 100, "y": 200, "width": 300, "height": 20}],
            "snickers": [],
            "puddles": [],
            "buttons": [],
            "doors": [],
            "exit_doors": [],
            "computers": [],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as file:
            json.dump(data, file)
            path = file.name
        try:
            level = load_level(path)
            self.assertEqual(len(level.platforms), 1)
            self.assertEqual(level.platforms[0].rect.x, 100)
            self.assertEqual(level.platforms[0].rect.width, 300)
        finally:
            os.remove(path)

    @patch("pygame.image.load")
    def test_load_level_creates_snickers(self, mock_load):
        image = pygame.Surface((50, 30))
        mock_load.return_value.convert_alpha.return_value = image
        data = {
            "player_1_start": {"x": 0, "y": 0},
            "player_2_start": {"x": 50, "y": 0},
            "platforms": [],
            "snickers": [{"x": 100, "y": 200, "color": "blue", "player_number": 1}],
            "puddles": [],
            "buttons": [],
            "doors": [],
            "exit_doors": [],
            "computers": [],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as file:
            json.dump(data, file)
            path = file.name
        try:
            level = load_level(path)
            self.assertEqual(len(level.snickers), 1)
            self.assertEqual(level.snickers[0].player_number, 1)
        finally:
            os.remove(path)

    def test_list_levels_sorts_by_level_number(self):
        with tempfile.TemporaryDirectory() as directory:
            filenames = ["level_3.json", "level_1.json", "level_2.json"]
            for filename in filenames:
                with open(os.path.join(directory, filename), "w") as file:
                    file.write("{}")
            levels = list_levels(directory)
            self.assertEqual(
                [os.path.basename(path) for path in levels],
                ["level_1.json", "level_2.json", "level_3.json"],
            )


if __name__ == "__main__":
    unittest.main()
