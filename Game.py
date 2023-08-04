import pygame
from pygame.locals import *
import random
def main():
    pygame.init()
    display = pygame.display.set_mode((400, 650))
    pygame.display.set_caption("Game")

    def event_handler():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    while True:
        event_handler()
        pygame.display.update()






if __name__ == "__main__":
    main()
