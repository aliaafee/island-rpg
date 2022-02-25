
import pygame
from ..camera import Camera
from ..math import Vector3
from .actor import Actor


class Grid(Actor):
    def __init__(self, size=(10, 5), **kargs) -> None:
        super().__init__(**kargs)
        self.size = size

    
    def transform(self, camera: Camera) -> None:
        super().transform(camera)

        points = []

        for x in range(self.size[0] + 1):
            points.append(Vector3(x* 10, 0, 0))
            points.append(Vector3(x* 10,  self.size[1] * 10, 0))

        for y in range(self.size[1] + 1):
            points.append(Vector3(0, y* 10, 0))
            points.append(Vector3(self.size[0] * 10, y* 10, 0))


        self.points_t = [camera.transform(p + self.position).xy for p in points]


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        for a, b in zip(*[iter(self.points_t)]*2):
            pygame.draw.line(screen, 'red', a, b)