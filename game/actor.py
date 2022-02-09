import pygame
import random
import math
from .math import Vector3, TransformMatrix, Vector2

class Actor:
    def __init__(self, groups = []) -> None:
        self.position = Vector3(0, 0, 0)
        self.screen_position = Vector3(0, 0, 0)
        self.screen_base_position = Vector3(0, 0, 0)
        #self.screen_rect = pygame.Rect(0, 0, 64, 64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.base_line = Vector2(1, -1)
        self.base_line.normalize()

        for group in groups:
            group.append(self)

    def update(self) -> None:
        pass

    def transform(self, transformation: TransformMatrix, translation: Vector3) -> None:
        self.screen_position = (transformation * self.position) + translation
        self.screen_base_position = (transformation * Vector3(self.position.x, self.position.y, 0)) + translation
        #self.screen_rect.center = self.screen_position.xy

    def draw_shadow(self, screen: pygame.surface.Surface):
        shadow_rect = pygame.rect.Rect(0,0,60, 30)
        shadow_rect.center = self.screen_base_position.xy
        pygame.draw.ellipse(
            screen,
            'grey',
            shadow_rect
        )

    def draw(self, screen: pygame.surface.Surface):
        self.draw_shadow(screen)
        pygame.draw.circle(
            screen, 
            self.color, 
            (self.screen_position.x, self.screen_position.y-30), 30
        )
        pygame.draw.circle(
            screen, 
            self.color, 
            (self.screen_position.x, self.screen_position.y-60), 30
        )



    