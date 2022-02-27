import pygame
import random
import math
from ..math import Vector3
from ..camera import Camera


class Actor:
    def __init__(self, position = Vector3(0, 0, 0), size = Vector3(1, 1, 1), groups = []) -> None:
        self.position = position
        self.size = size
        
        self.screen_position = Vector3(0, 0, 0)
        self.screen_base_position = Vector3(0, 0, 0)

        for group in groups:
            group.append(self)


    @property
    def base_position(self) -> Vector3:
        return Vector3(self.position.x, self.position.y, 0)


    def get_final_position(self):
        """
        Return the final expected position of the actor, if moving,
        otherwise return the current position. Used for centering the 
        camera on the actor
        """
        return self.position


    def set_topleft_position(self, position):
        self.position = position + Vector3(self.size.x, self.size.y, 0)/2


    def update(self, level) -> None:
        pass


    def start_interaction(self, actor) -> None:
        """
        Interaction between actors
        """
        pass


    def interaction_completed(self) -> bool:
        """
        Return true when self has finised interacting
        """
        return True


    def transform(self, camera: Camera) -> None:
        self.screen_position = camera.transform(self.position)
        self.screen_base_position = camera.transform(Vector3(self.position.x, self.position.y, 0))


    def draw_shadow(self, screen: pygame.surface.Surface):
        shadow_rect = pygame.rect.Rect(0,0,60, 30)
        shadow_rect.center = self.screen_base_position.xy
        pygame.draw.ellipse(
            screen,
            'grey',
            shadow_rect
        )


    def draw(self, screen: pygame.surface.Surface):
        if self.position.z != 0:
            pygame.draw.line(screen, 'blue', self.screen_position.xy, self.screen_base_position.xy)