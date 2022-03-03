import imp
import imp
import pygame
import sys
from .debug import debug
from .level import Level
from .level_editor import LevelEditor
from .massive_level import MassiveLevel
from .world import World


class Game:
    def __init__(self) -> None:
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("OrthoGame")
        self.clock = pygame.time.Clock()

        #self.level = Level()
        #self.level = LevelEditor()
        #self.level = MassiveLevel()
        self.level = World()


    def run(self):
        while True:
            self.level.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.level.mouse_clicked(event)
                if event.type == pygame.KEYUP:
                    self.level.key_pressed(event)

            self.level.transform()

            self.screen.fill('white')
            self.level.draw()

            debug(round(self.clock.get_fps()))

            pygame.display.update()
            self.clock.tick(self.fps)