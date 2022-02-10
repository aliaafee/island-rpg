import pygame
import random
import math
from .math import Vector3, TransformMatrix, Vector2

class Actor:
    def __init__(self, groups = []) -> None:
        self.position = Vector3(0, 0, 0)
        self.screen_position = Vector3(0, 0, 0)
        self.screen_base_position = Vector3(0, 0, 0)
        self.hit_radius = 30
    
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.base_line = Vector2(1, -1)
        self.base_line.normalize()

        for group in groups:
            group.append(self)


    def hitbox_sdf(self, point: Vector3) -> float:
        return self.position.distance_to(point) - self.hit_radius


    def hitbox_collision(self, obstacle) -> bool:
        distance = (
            self.hitbox_sdf(obstacle.position) 
            + obstacle.hitbox_sdf(self.position) 
            - self.position.distance_to(obstacle.position)
        )
        if distance < 0:
            return True
        return False


    def hitbox_collision_point(self, obstacle) -> Vector3:
        to_obstacle_sdf = obstacle.hitbox_sdf(self.position)
        to_obstacle_vec = (self.position - obstacle.position)
        distance = (
            to_obstacle_sdf
            + obstacle.hitbox_sdf(self.position) 
            - to_obstacle_vec.length()
        )
        if distance < 0:
            to_obstacle_vec.normalize_ip()
            return to_obstacle_vec * to_obstacle_sdf
        return None


    def update(self, obstacles: list) -> None:
        pass


    def transform(self, transformation: TransformMatrix, translation: Vector3) -> None:
        self.screen_position = (transformation * self.position) + translation
        self.screen_base_position = (transformation * Vector3(self.position.x, self.position.y, 0)) + translation


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