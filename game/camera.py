import math
from .math import Vector3, Matrix3x3, intersect_plane
from .statemachine import StateMachine


class Camera:
    def __init__(self, position: Vector3, origin: Vector3, screen_tile_size: tuple, world_grid_size: float) -> None:
        self._origin = origin
        self._position  = position
        self.screen_tile_size = screen_tile_size
        self.world_grid_size = world_grid_size

        self._ground_normal = Vector3(0, 0, 1)

        self._calculate_matrix()
        self._calculate_translation()

        self.follow_speed = 1

        self.statemachine = StateMachine("idle")
        self.statemachine.add_state("idle", self.idle_state)
        self.statemachine.add_state("moving", self.moving_state)


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
        tile_width, tile_height = self.screen_tile_size
        w_h = tile_width / 2
        h_h = tile_height / 2
        l = w_h/ math.cos(45/180 * math.pi)
        s = Vector3(self.world_grid_size, self.world_grid_size, self.world_grid_size)
        self._transform_matrix = Matrix3x3([
            [                              w_h/s.x,                          -1 * w_h/s.y,                       0],
            [                              h_h/s.x,                               h_h/s.y,              -1 * l/s.z],
            [ w_h * math.tan(45/180 * math.pi)/s.x,  w_h * math.tan(45/180 * math.pi)/s.y,                       0]
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


    def update(self, follow_actor=None):
        self.statemachine.update(follow_actor)


    def idle_state(self, follow_actor, first_run=False):
        if first_run:
            print("camera to idle")

        if follow_actor:
            if self.position.distance_to(follow_actor.position) > 50:
                return "moving"

        return "idle"


    def generate_steps(self, start: Vector3, end: Vector3):
        direction = (end - start)
        if direction.length() != 0:
            direction = direction.normalize()
        velocity = direction * self.follow_speed
        total_steps = int(end.distance_to(start) / self.follow_speed)
        for step in range(total_steps):
            yield step, velocity


    def moving_state(self, follow_actor, first_run=False):
        if first_run:
            print("Start Camera Pan")
            self.end_position = Vector3(follow_actor.position)
            self.path_generator = self.generate_steps(self.position, follow_actor.position)
            return "moving"

        try:
            step, velocity = next(self.path_generator)
        except StopIteration:
            return "idle"

        #if self.end_position != follow_actor.position and step > 5:
        #    return "idle"

        self.position = self.position + velocity

        

        return "moving"



# This camera can be rotated and tiled arbitarily, is probably broken now
# The camera class above should be used
# class RotateCamera(Camera):
#     def __init__(self, position: Vector3, origin: Vector3, rotation_deg: float, tilt_deg: float) -> None:
#         self._origin = origin
#         self._position  = position
#         self._rotation = (rotation_deg/180) * math.pi
#         self._tilt = (tilt_deg/180) * math.pi

#         self._ground_normal = Vector3(0, 0, 1)

#         self._calculate_matrix()
#         self._calculate_translation()


#     @property
#     def position(self) -> Vector3:
#         return self._position
#     @position.setter
#     def position(self, position: Vector3):
#         self._position = position
#         self._calculate_translation()


#     def _calculate_translation(self):
#         self._translation = self._origin - (self._transform_matrix * self._position)


#     def _calculate_matrix(self):
#         self._transform_matrix = Matrix3x3([
#                 [                      math.sin(self._rotation),                  -1 * math.sin(self._rotation),                        0],
#                 [math.cos(self._tilt) * math.sin(self._rotation), math.cos(self._tilt) * math.cos(self._rotation), -1 * math.sin(self._tilt)],
#                 [math.sin(self._tilt) * math.sin(self._rotation), math.sin(self._tilt) * math.cos(self._rotation),      math.cos(self._tilt)]
#             ])

#         self._inverse_transform_matrix = self._transform_matrix.inverse()

#         self._camera_direction = self._inverse_transform_matrix * Vector3(0, 0, 1)


#     def pan(self, direction: Vector3) -> None:
#         self.position = self.position + self._inverse_transform_matrix * direction


#     def transform(self, point: Vector3) ->Vector3:
#         """Transform point from World Space to Screen Space"""
#         return self._transform_matrix * point + self._translation

    
#     def inverse_transform(self, point: Vector3) -> Vector3:
#         """Transform point from Screen Space to World Space"""
#         return self._inverse_transform_matrix * (point - self._translation)


#     def project_ground(self, screen_point: Vector3, ground_elevation: int = 0) -> Vector3:
#         """Project a screen point on to the ground plane"""
#         return intersect_plane(
#             n=self._ground_normal,
#             p0=Vector3(0, 0, ground_elevation),
#             l0=self.inverse_transform(screen_point),
#             l=self._camera_direction
#         )