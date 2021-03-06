import pygame
from ..math import Vector3, Vector2
from ..camera import Camera
from .actor import Actor


class StaticActor(Actor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        self.image = None
        self.image_rect = pygame.rect.Rect(0, 0, 64, 64)
        self.image_offset = Vector2(0, 0)


    def set_image(self, image: pygame.surface.Surface) -> None:
        self.image = image
        self.image_rect = image.get_rect()


    def transform(self, camera: Camera) -> None:
        super().transform(camera)
        self.image_rect.center = self.screen_position.xy
        self.image_rect.bottom = self.screen_position.y
        self.image_rect.center = self.image_offset + self.image_rect.center


    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.image:
            screen.blit(self.image, self.image_rect)
        super().draw(screen)
        
        