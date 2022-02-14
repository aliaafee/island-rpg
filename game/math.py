import pygame

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

    def inverse(self):
        """Thanks Alok Aryan on stackoverflow"""
        det_ = self.matrix[0][0] * (
                (self.matrix[1][1] * self.matrix[2][2]) - (self.matrix[1][2] * self.matrix[2][1])) - \
            self.matrix[0][1] * (
                    (self.matrix[1][0] * self.matrix[2][2]) - (self.matrix[1][2] * self.matrix[2][0])) + \
            self.matrix[0][2] * (
                    (self.matrix[1][0] * self.matrix[2][1]) - (self.matrix[1][1] * self.matrix[2][0]))
        co_fctr_1 = [(self.matrix[1][1] * self.matrix[2][2]) - (self.matrix[1][2] * self.matrix[2][1]),
                    -((self.matrix[1][0] * self.matrix[2][2]) - (self.matrix[1][2] * self.matrix[2][0])),
                    (self.matrix[1][0] * self.matrix[2][1]) - (self.matrix[1][1] * self.matrix[2][0])]

        co_fctr_2 = [-((self.matrix[0][1] * self.matrix[2][2]) - (self.matrix[0][2] * self.matrix[2][1])),
                    (self.matrix[0][0] * self.matrix[2][2]) - (self.matrix[0][2] * self.matrix[2][0]),
                    -((self.matrix[0][0] * self.matrix[2][1]) - (self.matrix[0][1] * self.matrix[2][0]))]

        co_fctr_3 = [(self.matrix[0][1] * self.matrix[1][2]) - (self.matrix[0][2] * self.matrix[1][1]),
                    -((self.matrix[0][0] * self.matrix[1][2]) - (self.matrix[0][2] * self.matrix[1][0])),
                    (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])]

        return Matrix3x3([[1 / det_ * (co_fctr_1[0]), 1 / det_ * (co_fctr_2[0]), 1 / det_ * (co_fctr_3[0])],
                    [1 / det_ * (co_fctr_1[1]), 1 / det_ * (co_fctr_2[1]), 1 / det_ * (co_fctr_3[1])],
                    [1 / det_ * (co_fctr_1[2]), 1 / det_ * (co_fctr_2[2]), 1 / det_ * (co_fctr_3[2])]])


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


def intersect_plane(n: Vector3, p0: Vector3, l0: Vector3, l: Vector3) -> Vector3:
    """Ray plane intersection. intersection is infront of ray it t is positive"""
    denom = n.dot(l)
    if denom:
        p0l0 = p0 - l0
        t = p0l0.dot(n) / denom
        return l0 + (l * t)
    return None
