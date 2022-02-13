import pygame
from .actor import Actor


class Mouse(Actor):
    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.circle(screen, (200, 0, 0), self.screen_position.xy, 10)
        return super().draw(screen)