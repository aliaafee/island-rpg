import pygame
from .math import Vector2, Vector3, TransformMatrix
from .animated_actor import AnimatedActor
from .resources import load_image, load_image_folder

class Player(AnimatedActor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)

        self.hitbox = Vector3(30, 30, 30)
        self.hitbox_offset = Vector3(0, 0, 30)
        
        self.direction = Vector3()
        self.speed = 3
        
        self.current_direction = "down"
        self.current_action = "idle"

        animation_names = [
            'up_walking', 'down_walking', 'left_walking', 'right_walking',
            'up_idle', 'down_idle', 'left_idle', 'right_idle',
            'up_attack', 'down_attack', 'left_attack', 'right_attack'
        ]
        for animation_name in animation_names:
            self.add_animation(animation_name, load_image_folder('player', animation_name))
        self.set_current_animation("down_idle")


    def hitbox_sd(self, point: Vector3) -> float:
        return self.sd_sphere(point, 30)
        

    def update(self, obstacles: list) -> None:
        super().update(obstacles)

        self.input(obstacles)
        
        self.set_current_animation("{}_{}".format(self.current_direction, self.current_action))
        self.animate()

        

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
        elif keys[pygame.K_a]:
            self.direction.z = 1
        else:
            self.direction.z = 0

        if self.direction.length() > 0:
            self.direction.normalize_ip()
            self.current_action = "walking"
        else:
            self.current_action = "idle"

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


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        super().draw_shadow(screen)
        self.draw_animation(screen)
        