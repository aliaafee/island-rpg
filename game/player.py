import pygame
from .math import Vector2, Vector3
from .camera import Camera
from .animated_actor import AnimatedActor
from .resources import load_image, load_image_folder

class PlayerState:
    def __init__(self, player) -> None:
        self.player = player

    def enter(self):
        pass

    def update(self, obstacles: list):
        pass

    def exit(self):
        pass


class WalkState(PlayerState):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.end =Vector3(0, 0, 0)
        self.speed = 3
        self.step = Vector3(0, 0, 0)
        self.total_step_count = 0
        self.step_count = 0

    def enter(self):
        super().enter()
        direction = self.end - self.player.position
        direction.normalize_ip()
        self.step = direction * self.speed
        distance = self.player.position.distance_to(self.end)
        if distance < self.speed:
            self.total_step_count = 0
            self.step_count = 0
            return
        self.total_step_count = distance / self.speed
        self.step_count = 0
        self.player.animation_action = "walking"
        if direction.x > 0 and direction.y < 0:
            self.player.animation_direction = "right"
        elif direction.x > 0 and direction.y > 0:
            self.player.animation_direction = "down"
        elif direction.x < 0 and direction.y > 0:
            self.player.animation_direction = "left"
        else:
            self.player.animation_direction = "up"

    def update(self, obstacles: list):
        super().update(obstacles)
        if self.step_count < self.total_step_count:
            self.player.position = self.player.position + self.step
            self.step_count += 1
        else:
            self.player.transition_state(None)

    
    def exit(self):
        self.player.animation_action = "idle"




class Player(AnimatedActor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)

        self.hitbox = Vector3(30, 30, 30)
        self.hitbox_offset = Vector3(0, 0, 30)
        
        self.direction = Vector3()
        self.speed = 3
        
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

        self.state_walk_x = PlayerState(self)

        self.walk_to_state = WalkState(self)

        self.state = None


    def transition_state(self, state: PlayerState):
        if self.state:
            self.state.exit()
        self.state = state
        if self.state:
            self.state.enter()


    def walk_to(self, point: Vector3):
        self.walk_to_state.end = point
        self.transition_state(self.walk_to_state)


    def hitbox_sd(self, point: Vector3) -> float:
        return self.sd_sphere(point, 30)
        

    def update(self, obstacles: list) -> None:
        super().update(obstacles)
        self.input(obstacles)

        if self.state:
            self.state.update(obstacles)
        
        self.set_current_animation("{}_{}".format(self.animation_direction, self.animation_action))
        self.animate()
        

    def input(self, obstacles: list) -> None:
        keys = pygame.key.get_pressed()
        """
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
        """

    def transform(self, camera: Camera) -> None:
        super().transform(camera)


    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        super().draw_shadow(screen)
        self.draw_animation(screen)
        