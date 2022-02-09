import pygame
import math

Vector3 = pygame.math.Vector3

Vector2 = pygame.math.Vector2


class TransformMatrix:
    def __init__(self, matrix) -> None:
        """
            Matrix format = [
                [a, b, c],
                [d, e, f],
                [g, h, i]
            ]
        """
        self.matrix = matrix
        pass

    def __mul__(self, vec3: Vector3) -> Vector3:
        return Vector3(
            self.matrix[0][0] * vec3.x + self.matrix[0][1] * vec3.y + self.matrix[0][2] * vec3.z,
            self.matrix[1][0] * vec3.x + self.matrix[1][1] * vec3.y + self.matrix[1][2] * vec3.z,
            self.matrix[2][0] * vec3.x + self.matrix[2][1] * vec3.y + self.matrix[2][2] * vec3.z
        )