import pygame
from .math import Vector3, Vector2, Transformation
from .actor import Actor


class AnimatedActor(Actor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = None
        self.image_rect = pygame.rect.Rect(0, 0, 64, 64)
        self.image_offset = Vector2(0, 0)


    def add_animation(self, name: str, frames: list) -> None:
        self.animations[name] =  frames


    def set_current_animation(self, name: str) -> None:
        if not name in self.animations.keys():
            return
        self.current_animation = self.animations[name]
        if not self.current_animation:
            return
        self.image_rect = self.current_animation[0].get_rect()


    def animate(self) -> None:
        if not self.current_animation:
            return

        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.current_animation):
            self.current_frame = 0

        self.image = self.current_animation[int(self.current_frame)]


    def transform(self, transformation: Transformation) -> None:
        super().transform(transformation)
        self.image_rect.center = self.screen_position.xy
        self.image_rect.bottom = self.screen_position.y
        self.image_rect.center = self.image_offset + self.image_rect.center


    def draw_animation(self, screen: pygame.surface.Surface) -> None:
        if not self.image:
            return
        screen.blit(self.image, self.image_rect)
    