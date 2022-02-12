import pygame
import math

Vector3 = pygame.math.Vector3

Vector2 = pygame.math.Vector2


class Matrix3x3:
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


def vector2_abs(a: Vector2) -> Vector2:
    return Vector2(
        abs(a.x),
        abs(a.y)
    )


def vector3_abs(a: Vector3) -> Vector3:
    return Vector3(
        abs(a.x),
        abs(a.y),
        abs(a.z)
    )


def vector2_max(a: Vector2, b: Vector2) -> Vector2:
    return Vector2(
        max(a.x, b.x),
        max(a.y, b.y)
    )


def vector3_max(a: Vector3, b: Vector3) -> Vector3:
    return Vector3(
        max(a.x, b.x),
        max(a.y, b.y),
        max(a.z, b.z),
    )


class Transformation:
    def __init__(self, transformation: Matrix3x3, translation: Vector3) -> None:
        self.transformation = transformation
        self.translation = translation


    def transform(self, point: Vector3) -> Vector3:
        return self.transformation * point + self.translation