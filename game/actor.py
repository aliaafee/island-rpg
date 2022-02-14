import pygame
import random
import math
from .math import Vector3, Vector2, vector3_max, vector3_abs
from .camera import Camera

class Actor:
    def __init__(self, groups = []) -> None:
        self.position = Vector3(0, 0, 0)
        self.screen_position = Vector3(0, 0, 0)
        self.screen_base_position = Vector3(0, 0, 0)

        self.set_hitbox(Vector3(50, 50 , 50))
        self.show_hitbox = False
        self.screen_hitbox_points = []
    
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.base_line = Vector2(1, -1)
        self.base_line.normalize()

        for group in groups:
            group.append(self)


    def set_hitbox(self, hitbox: Vector3) -> None:
        self.hitbox = hitbox
        self.hitbox_offset = Vector3(0, 0, self.hitbox.z)


    def hitbox_sd(self, point: Vector3) -> float:
        return self.sd_box(point, self.hitbox)


    def sd_box(self, point: Vector3, box: Vector3) -> float:
        q = vector3_abs(point - self.hitbox_position()) - box
        return vector3_max(q, Vector3(0, 0, 0)).length() + min(max(q.x, max(q.y, q.z)), 0)


    def sd_sphere(self, point: Vector3, radius: float) -> float:
        q = point - self.hitbox_position()
        return q.length() - radius


    def hitbox_position(self):
        return self.position + self.hitbox_offset


    def hitbox_collision(self, obstacle) -> bool:
        distance = (
            self.hitbox_sd(obstacle.hitbox_position()) 
            + obstacle.hitbox_sd(self.hitbox_position()) 
            - self.hitbox_position().distance_to(obstacle.hitbox_position())
        )
        if distance < 0:
            return True
        return False


    def update(self, obstacles: list) -> None:
        pass


    def transform(self, camera: Camera) -> None:
        self.screen_position = camera.transform(self.position)
        self.screen_base_position = camera.transform(Vector3(self.position.x, self.position.y, 0))
        if self.show_hitbox:
            self.transform_hitbox(camera)


    def draw_shadow(self, screen: pygame.surface.Surface):
        shadow_rect = pygame.rect.Rect(0,0,60, 30)
        shadow_rect.center = self.screen_base_position.xy
        pygame.draw.ellipse(
            screen,
            'grey',
            shadow_rect
        )


    def transform_hitbox(self, camera: Camera) -> None:
        hbox = self.hitbox + self.hitbox_offset
        hitbox_points = [
            (hbox.x, hbox.y, hbox.z),
            (hbox.x, hbox.y * -1, hbox.z),
            (hbox.x * -1, hbox.y * -1, hbox.z),
            (hbox.x * -1, hbox.y, hbox.z),
            (hbox.x, hbox.y, hbox.z),
            (hbox.x, hbox.y, 0),
            (hbox.x, hbox.y * -1, 0),
            (hbox.x * -1, hbox.y * -1, 0),
            (hbox.x * -1, hbox.y, 0),
            (hbox.x, hbox.y, 0)
        ]
        self.screen_hitbox_points = [camera.transform(point + self.position).xy for point in hitbox_points]

    def draw_hitbox(self, screen: pygame.surface.Surface):
        pygame.draw.polygon(screen, 'red', self.screen_hitbox_points, 1)


    def draw(self, screen: pygame.surface.Surface):
        if self.show_hitbox:
            self.draw_hitbox(screen)