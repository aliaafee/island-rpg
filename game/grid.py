
import pygame
from .camera import Camera
from .math import Vector3
from .actor import Actor


class Grid(Actor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)

    
    def transform(self, camera: Camera) -> None:
        super().transform(camera)

        points = []

        for i in range(101):
            points.append(Vector3(i* 10, 0, 0))
            points.append(Vector3(i* 10,  1000, 0))

        for i in range(101):
            points.append(Vector3(0, i* 10, 0))
            points.append(Vector3(1000, i* 10, 0))


        self.points_t = [camera.transform(p + self.position).xy for p in points]


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        for a, b in zip(*[iter(self.points_t)]*2):
            pygame.draw.line(screen, 'red', a, b)