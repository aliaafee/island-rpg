import pygame

from game.actors.actor import Actor
from ..math import Vector2, Vector3
from ..camera import Camera
from .animated_actor import AnimatedActor
from ..resources import load_image, load_image_folder
from ..statemachine import StateMachine


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

        
        
        self.statemachine = StateMachine("idle")

        self.statemachine.add_state("idle", self.idle_state)
        
        self.walk_path = []
        self.walk_path_start = None
        self.statemachine.add_state("walking_path", self.walking_path_state)

        self.interact_target = None
        self.statemachine.add_state("interacting", self.interact_state)


    def idle_state(self, level, first_run=False):
        if first_run:
            print("Player to idle")
            self.animation_action = "idle"

        if self.walk_path:
            return 'walking_path'

        if self.interact_target:
            return 'interacting'

        return "idle"


    def get_direction_name(self, direction: Vector3):
        if direction.x >= 0 and direction.y < 0:
            return "right"
        elif direction.x >= 0 and direction.y >= 0:
            return "down"
        elif direction.x < 0 and direction.y >= 0:
            return "left"
        return "up"


    def generate_steps(self, path: list):
        for node in path:
            direction = (node - self.position)
            if direction.length() != 0:
                direction = direction.normalize() * self.speed
            total_steps = int(self.position.distance_to(node) / self.speed)
            self.animation_action = "walking"
            self.animation_direction = self.get_direction_name(direction)
            for step in range(total_steps):
                yield direction


    def walking_path_state(self, level, first_run=False):
        if first_run:
            print("Player to walking")
            if not self.walk_path:
                return "idle"

            self.walk_path_start = Vector3(self.position)
            self.current_path = self.walk_path
            self.path_generator = self.generate_steps(self.walk_path)

        if self.walk_path != self.current_path:
            #if path changed while walking switch to idle state
            return "idle"
        try:
            
            self.position += next(self.path_generator)
        except StopIteration:
            self.position = Vector3(self.walk_path[-1])
            self.walk_path_start = None
            self.walk_path = []
            return "idle"
        return "walking_path"


    def walk_to(self, point: Vector3):
        self.walk_path.append(point)


    def walk_on_path(self, path: list):
        if self.interact_target:
            return
        self.walk_path = path


    def get_final_position(self):
        if self.walk_path:
            return self.walk_path[-1]
        return self.position


    def stop_walking(self):
        self.walk_path = []
        self.walk_path_start = None


    def interact_state(self, level, first_run=False):
        if first_run:
            print("Player started interacting with {}.".format(self.interact_target))
            if not self.interact_target.at_interactable_position(self):
                print("Player is too far")
                path = level.pathfinder.find_path(
                    self.position,
                    self.interact_target.get_interact_position(self)
                )
                if path:
                    print("Player walking to target")
                    self.walk_path = path
                    return "walking_path"
                self.interact_target = None
                print("Player cannot find a path to target")
                return "idle"
            self.interact_target.start_interaction(self)
            self.animation_action = "attack"
            self.animation_direction = self.get_direction_name(self.interact_target.position - self.position)
            return "interacting"

        if self.interact_target.interaction_completed(self):
            print("Player interaction completed with {}".format(self.interact_target))
            self.interact_target = None
            return 'idle'

        return 'interacting'


    def interact_with(self, target: Actor):
        if self.interact_target:
            return
        self.stop_walking()
        self.interact_target = target


    def update(self, level) -> None:
        super().update(level)

        self.input(level)

        self.statemachine.update(level)
        
        self.set_current_animation("{}_{}".format(self.animation_direction, self.animation_action))
        self.animate()


    def input(self, obstacles: list) -> None:
        keys = pygame.key.get_pressed()


    def transform(self, camera: Camera) -> None:
        super().transform(camera)
        if self.walk_path_start:
            self.screen_walk_path = [camera.transform(p) for p in [self.walk_path_start] + self.walk_path]
        else:
            self.screen_walk_path = None


    def draw(self, screen: pygame.surface.Surface):
        if self.screen_walk_path:
            pygame.draw.lines(screen, 'silver',False, [p.xy for p in self.screen_walk_path])
        super().draw(screen)
        super().draw_shadow(screen)
        self.draw_animation(screen)