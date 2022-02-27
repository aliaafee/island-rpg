import math
import pygame
from ..math import Vector3
from ..camera import Camera
from .static_actor import StaticActor


class Ground(StaticActor):
    def __init__(self, cell_count=(10, 10), cell_size=10, **kargs) -> None:
        super().__init__(**kargs)
        self.cell_count = cell_count
        self.cell_size = cell_size

        width, height = self.cell_count
        self.grid = [
            [None for x in range(width)] for y in range(height)
        ]


    def set_cell_image(self, position: Vector3, image):
        x = math.floor(position.x / self.cell_size)
        y = math.floor(position.y / self.cell_size)

        if x > self.cell_count[0] - 1 or y > self.cell_count[1] - 1:
            return

        self.grid[y][x] = image


    def transform(self, camera: Camera) -> None:
        super().transform(camera)
        self.i_hat = camera.transform_direction(Vector3(self.cell_size, 0, 0))
        self.j_hat = camera.transform_direction(Vector3(0, self.cell_size, 0))


    def draw(self, screen: pygame.surface.Surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    cell_pos = self.screen_position + self.i_hat * x + self.j_hat * y
                    cell_rect = cell.get_rect()
                    cell_rect.center = cell_pos.xy
                    screen.blit(cell, cell_rect)



