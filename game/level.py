import pygame
import math
from .actor import Actor
from .player import Player
from .math import TransformMatrix, Vector3


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []

        self.load_level()
        


    def load_level(self) -> None:
        alpha = (45/180) * math.pi
        beta = (60/180) * math.pi
        self.transformation = TransformMatrix([
            [                 math.sin(alpha),             -1 * math.sin(alpha),                   0],
            [math.cos(beta) * math.sin(alpha), math.cos(beta) * math.cos(alpha), -1 * math.sin(beta)],
            [math.sin(beta) * math.sin(alpha), math.sin(beta) * math.cos(alpha),      math.cos(beta)]
        ])

        self.translation = pygame.Vector3(
            self.display_surface.get_width()/2, 
            self.display_surface.get_height()/2,
            0
        )

        self.player = Player([self.visible_actors])
        self.player.position = Vector3(100, 100, 0)

        self.obstacle = Actor([self.visible_actors])
        self.obstacle.position = Vector3(0, 0, 0)
        
        

    def update(self) -> None:
        for actor in self.visible_actors:
            actor.update()

    def transform(self) -> None:
        for actor in self.visible_actors:
            actor.transform(self.transformation, self.translation)

    def draw(self) -> None:
        """Sorted according to distance between point and the line x + y = 0 on the ground plane"""
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: (actor.position.x + actor.position.y) / 1.4142135623730951):
            actor.draw(self.display_surface)