import pygame
from .actor import Actor
from ..math import Vector3
from ..camera import Camera


class Mouse(Actor):
    def transform(self, camera: Camera) -> None:
        super().transform(camera)


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        pygame.draw.circle(screen, (200, 0, 0), self.screen_position.xy, 2)