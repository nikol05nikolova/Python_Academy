from menu import Menu
from level_select import LevelSelect
from level_loader import list_levels
from game import Game


def main():
    menu = Menu()
    level_select = LevelSelect(list_levels())
    while True:
        menu.run()
        level_path = level_select.run()
        game = Game(level_path)
        game.run()


if __name__ == "__main__":
    main()
