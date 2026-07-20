import sys
import pygame
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Academy")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(x=100, y=100, width=40, height=60, color=(50, 120, 255))
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((30, 30, 30))
            self.player.move()
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()