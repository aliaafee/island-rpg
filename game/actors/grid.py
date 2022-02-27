
import pygame
from ..camera import Camera
from ..math import Vector3
from .actor import Actor


class Grid(Actor):
    def __init__(self, cell_count=(10, 5), cell_size=10, **kargs) -> None:
        super().__init__(**kargs)
        self.cell_count = cell_count
        self.cell_size = cell_size

    
    def transform(self, camera: Camera) -> None:
        super().transform(camera)

        points = []

        for x in range(self.cell_count[0] + 1):
            points.append(Vector3(x* self.cell_size, 0, 0))
            points.append(Vector3(x* self.cell_size,  self.cell_count[1] * self.cell_size, 0))

        for y in range(self.cell_count[1] + 1):
            points.append(Vector3(0, y* self.cell_size, 0))
            points.append(Vector3(self.cell_count[0] * self.cell_size, y * self.cell_size, 0))


        self.points_t = [camera.transform(p + self.position).xy for p in points]


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        for a, b in zip(*[iter(self.points_t)]*2):
            pygame.draw.line(screen, 'grey', a, b)