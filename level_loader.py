import os
import re
import json
from constants import *
from game_platform import Platform
from puddle import Puddle
from button import Button
from door import Door
from exit_door import ExitDoor
from computer import Computer
from snickers import Snickers

NAMED_COLORS = {
    "purple": PURPLE_COLOR,
    "pink": PINK_COLOR,
    "green": GREEN_COLOR,
    "red": RED_COLOR,
    "blue": PLAYER_1_COLOR,
    "yellow": PLAYER_2_COLOR,
}

BUTTON_IMAGES = {
    "purple": ("data/images/button_purple.png", "data/images/button_purple_pressed.png"),
    "pink": ("data/images/button_pink.png", "data/images/button_pink_pressed.png"),
    "green": ("data/images/button_green.png", "data/images/button_green_pressed.png"),
    "red": ("data/images/button_red.png", "data/images/button_red_pressed.png"),
}

PUDDLE_COLORS = {
    "blue": BLUE_PUDDLE_COLOR,
    "yellow": YELLOW_PUDDLE_COLOR,
    "green": GREEN_PUDDLE_COLOR,
}

PUDDLE_IMAGES = {
    "blue": "data/images/puddle_blue.png",
    "yellow": "data/images/puddle_yellow.png",
    "green": "data/images/puddle_green.png",
}

SNICKERS_IMAGES = {
    "blue": "data/images/snickers_blue.png",
    "yellow": "data/images/snickers_yellow.png",
}


class Level:
    def __init__(self, data):
        self.player_1_start = data["player_1_start"]
        self.player_2_start = data["player_2_start"]
        self.platforms = [
            Platform(
                p["x"],
                p["y"],
                p["width"],
                p["height"],
                PLATFORM_COLOR,
            )
            for p in data.get("platforms", [])
        ]
        self.snickers = [
            Snickers(
                s["x"],
                s["y"],
                SNICKERS_WIDTH,
                SNICKERS_HEIGHT,
                SNICKERS_IMAGES[s["color"]],
                s["player_number"],
            )
            for s in data.get("snickers", [])
        ]
        self.puddles = [
            Puddle(
                p["x"],
                p["y"],
                p["width"],
                PUDDLE_HEIGHT,
                PUDDLE_COLORS[p["type"]],
                PUDDLE_IMAGES[p["type"]],
                p["type"],
            )
            for p in data.get("puddles", [])
        ]
        self.buttons = [
            Button(
                b["x"],
                b["y"],
                b["width"],
                b["height"],
                NAMED_COLORS[b["color"]],
                *BUTTON_IMAGES[b["color"]],
            )
            for b in data.get("buttons", [])
        ]
        self.doors = [
            Door(
                d["x"],
                d["y"],
                d["width"],
                d["height"],
                NAMED_COLORS[d["color"]],
                self.buttons[d["button_index"]],
            )
            for d in data.get("doors", [])
        ]
        self.exit_doors = [
            ExitDoor(
                d["x"],
                d["y"],
                d["width"],
                d["height"],
                NAMED_COLORS[d["color"]],
                d["player_number"],
            )
            for d in data.get("exit_doors", [])
        ]
        self.computers = [
            Computer(c["x"], c["y"], c["width"], c["height"], (120, 120, 120))
            for c in data.get("computers", [])
        ]


def load_level(path):
    with open(path) as f:
        data = json.load(f)
    return Level(data)


def list_levels(directory="levels"):
    files = [f for f in os.listdir(directory) if f.endswith(".json")]

    def sort_key(filename):
        match = re.search(r"\d+", filename)
        return int(match.group()) if match else 0

    files.sort(key=sort_key)
    return [os.path.join(directory, f) for f in files]
