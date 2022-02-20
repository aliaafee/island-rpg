import pygame
from .math import Vector2, Vector3
from .camera import Camera
from .animated_actor import AnimatedActor
from .resources import load_image, load_image_folder
from .statemachine import StateMachine


class Player(AnimatedActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.direction = Vector3()
        self.speed = 1
        
        self.animation_direction = "down"
        self.animation_action = "idle"

        animation_names = [
            'up_walking', 'down_walking', 'left_walking', 'right_walking',
            'up_idle', 'down_idle', 'left_idle', 'right_idle',
            'up_attack', 'down_attack', 'left_attack', 'right_attack'
        ]
        for animation_name in animation_names:
            self.add_animation(animation_name, load_image_folder('player', animation_name))
        self.set_current_animation("down_idle")

        self.walk_path = []
        self.walk_path_start = None
        self.path_generator = None
        
        self.statemachine = StateMachine()
        self.statemachine.set_start("idle")

        self.statemachine.add_state("idle", self.idle_state)
        self.statemachine.add_state("walking_path", self.walking_path_state)


    def get_animation_direction_name(self, direction: Vector3):
        if direction.x >= 0 and direction.y < 0:
            return "right"
        elif direction.x >= 0 and direction.y >= 0:
            return "down"
        elif direction.x < 0 and direction.y >= 0:
            return "left"
        return "up"


    def idle_state(self, obstacles):
        if self.walk_path:
            self.path_generator = self.generate_path(self.walk_path)
            return 'walking_path'

        self.animation_action = "idle"
        return "idle"


    def walking_path_state(self, obstacles):
        try:
            self.position += next(self.path_generator)
        except StopIteration:
            self.position = Vector3(self.walk_path[-1])
            self.walk_path = []
            return "idle"
        return "walking_path"


    def generate_path(self, path: list):
        for node in path:
            direction = (node - self.position)
            if direction.length() != 0:
                direction = direction.normalize() * self.speed
            total_steps = int(self.position.distance_to(node) / self.speed)
            self.animation_action = "walking"
            self.animation_direction = self.get_animation_direction_name(direction)
            for step in range(total_steps):
                yield direction


    def walk_to(self, point: Vector3):
        if not(self.walk_path):
            self.walk_path_start = Vector3(self.position)
        self.walk_path.append(point)


    def walk_on_path(self, path: list):
        self.statemachine.set_current_state("idle")
        self.walk_path_start = Vector3(self.position)
        self.walk_path = path


    def update(self, obstacles: list) -> None:
        super().update(obstacles)
        self.input(obstacles)

        self.statemachine.update(obstacles)
        
        self.set_current_animation("{}_{}".format(self.animation_direction, self.animation_action))
        self.animate()
        

    def input(self, obstacles: list) -> None:
        keys = pygame.key.get_pressed()


    def transform(self, camera: Camera) -> None:
        super().transform(camera)
        if self.walk_path:
            self.screen_walk_path = [camera.transform(p) for p in [self.walk_path_start] + self.walk_path]


    def draw(self, screen: pygame.surface.Surface):
        if self.walk_path:
            pygame.draw.lines(screen, 'red',False, [p.xy for p in self.screen_walk_path])
        super().draw(screen)
        super().draw_shadow(screen)
        self.draw_animation(screen)

        
        