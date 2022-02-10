import pygame
from .math import Vector2, Vector3, TransformMatrix
from .actor import Actor
from .resources import load_image

class Player(Actor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)
        self.direction = Vector3()
        self.speed = 3
        self.image = load_image("test", "player.png")
        self.image_rect = self.image.get_rect()
        

    def update(self, obstacles: list) -> None:
        super().update(obstacles)
        self.input(obstacles)
        

    def input(self, obstacles: list) -> None:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.current_direction = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.current_direction = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.current_direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.current_direction = "right"
        else:
            self.direction.x = 0

        if keys[pygame.K_z]:
            self.direction.z = -1
            self.current_direction = "down"
        elif keys[pygame.K_a]:
            self.direction.z = 1
            self.current_direction = "up"
        else:
            self.direction.z = 0

        if self.direction.length() > 0:
            self.direction.normalize()

        self.direction = self.direction.rotate_z(-45)

        initial_position = self.position
        
        self.position = self.position +  (self.direction * self.speed)

        if self.position.z < 0:
            self.position.z = 0

        for obstacle in obstacles:
            if self.hitbox_collision(obstacle):
                self.position = initial_position
        

    def transform(self, transformation: TransformMatrix, translation: Vector3) -> None:
        super().transform(transformation, translation)
        self.image_rect.center = self.screen_position.xy
        self.image_rect.bottom = self.screen_position.y


    def draw(self, screen: pygame.surface.Surface):
        super().draw_shadow(screen)
        screen.blit(self.image, self.image_rect)
        