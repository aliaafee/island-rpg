import math
from .math import Vector3, Matrix3x3, intersect_plane


class Camera:
    def __init__(self, position: Vector3, origin: Vector3, rotation_deg: float, tilt_deg: float) -> None:
        self._origin = origin
        self._position  = position
        self._rotation = (rotation_deg/180) * math.pi
        self._tilt = (tilt_deg/180) * math.pi

        self._ground_normal = Vector3(0, 0, 1)

        self._calculate_matrix()
        self._calculate_translation()


    @property
    def position(self) -> Vector3:
        return self._position
    @position.setter
    def position(self, position: Vector3):
        self._position = position
        self._calculate_translation()


    def _calculate_translation(self):
        self._translation = self._origin - (self._transform_matrix * self._position)


    def _calculate_matrix(self):
        self._transform_matrix = Matrix3x3([
                [                      math.sin(self._rotation),                  -1 * math.sin(self._rotation),                        0],
                [math.cos(self._tilt) * math.sin(self._rotation), math.cos(self._tilt) * math.cos(self._rotation), -1 * math.sin(self._tilt)],
                [math.sin(self._tilt) * math.sin(self._rotation), math.sin(self._tilt) * math.cos(self._rotation),      math.cos(self._tilt)]
            ])

        self._inverse_transform_matrix = self._transform_matrix.inverse()

        self._camera_direction = self._inverse_transform_matrix * Vector3(0, 0, 1)


    def pan(self, direction: Vector3) -> None:
        self.position = self.position + self._inverse_transform_matrix * direction


    def transform(self, point: Vector3) ->Vector3:
        """Transform point from World Space to Screen Space"""
        return self._transform_matrix * point + self._translation

    
    def inverse_transform(self, point: Vector3) -> Vector3:
        """Transform point from Screen Space to World Space"""
        return self._inverse_transform_matrix * (point - self._translation)


    def project_ground(self, screen_point: Vector3, ground_elevation: int = 0) -> Vector3:
        """Project a screen point on to the ground plane"""
        return intersect_plane(
            n=self._ground_normal,
            p0=Vector3(0, 0, ground_elevation),
            l0=self.inverse_transform(screen_point),
            l=self._camera_direction
        )
        