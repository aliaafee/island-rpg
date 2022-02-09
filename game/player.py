import pygame
from .math import Vector2, Vector3, TransformMatrix
from .actor import Actor
from .resources import load_image

class Player(Actor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)
        self.direction = Vector3()
        self.speed = 3
        #self.points = [
        #    Vector3(50, 50, 0),
        #    Vector3(50, -50, 0),
        #    Vector3(-50, -50, 0),
        #    Vector3(-50, 50, 0)
        #]
        self.image = load_image("test", "player.png")
        self.image_rect = self.image.get_rect()
        

    def update(self) -> None:
        self.input()
        return super().update()

    def input(self) -> None:
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
        
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed
        self.position.z += self.direction.z * self.speed

        if self.position.z < 0:
            self.position.z = 0

    def transform(self, transformation: TransformMatrix, translation: Vector3) -> None:
        #self.transformed_points = []
        #for point in self.points:
        #    self.transformed_points.append(
        #        ((transformation * (point + (self.position.x, self.position.y, 0))) + translation).xy
        #    )
        super().transform(transformation, translation)
        self.image_rect.center = self.screen_position.xy
        self.image_rect.bottom = self.screen_position.y


    def draw(self, screen: pygame.surface.Surface):
        #pygame.draw.polygon(screen, (0, 255, 0), self.transformed_points, 1)
        super().draw_shadow(screen)
        screen.blit(self.image, self.image_rect)
        