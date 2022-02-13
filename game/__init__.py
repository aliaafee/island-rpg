import imp
import imp
import pygame
import sys
from .debug import debug
from .level import Level
#from .helpers import debug


class Game:
    def __init__(self) -> None:
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("OrthoGame")
        self.clock = pygame.time.Clock()

        self.level = Level()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('white')

            self.level.update()
            self.level.transform()
            self.level.draw()

            #debug(round(self.clock.get_fps()))

            pygame.display.update()
            self.clock.tick(self.fps)