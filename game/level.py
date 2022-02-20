import pygame

from .player import Player
from .vegetation import Tree
from .rock import Rock
from .mouse import Mouse
from .math import Vector3
from .camera import Camera
from .debug import debug
from .pathfinder import Pathfinder
from .box import Box


test_map = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

test_grid_size = 60


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []
        self.obstacles = []

        self.load_level()


    def load_level(self) -> None:
        self.camera = Camera(
            position=Vector3(300, 300, 0),
            origin=Vector3(
                self.display_surface.get_width()/2, 
                self.display_surface.get_height()/2,
                0
            ),
            rotation_deg=45,
            tilt_deg=60
        )

        for y, row in enumerate(test_map):
            for x, cell in enumerate(row):
                if cell == 0:
                    rock = Box(groups=[self.visible_actors, self.obstacles])
                    rock.size = Vector3(60, 60, 60)
                    rock.set_topleft_position(Vector3(x * test_grid_size , y * test_grid_size , 0))

        self.player = Player(groups=[self.visible_actors])
        self.player.position = Vector3(120, 60, 0)

        self.mouse = Mouse(groups=[self.visible_actors])

        self.pathfinder = Pathfinder((600, 600), (10,10))
        self.pathfinder.add_obstacles(
            [(o.position, o.size) for o in self.obstacles]
        )


    def input(self) -> None:
        keys = pygame.key.get_pressed()

        pan = Vector3(0,0,0)
        if keys[pygame.K_UP]:
            pan.y -= 2
        elif keys[pygame.K_DOWN]:
            pan.y += 2
        elif keys[pygame.K_LEFT]:
            pan.x -= 2
        elif keys[pygame.K_RIGHT]:
            pan.x += 2
        if pan.length_squared != 0:
            self.camera.pan(pan)

        mouse_position = pygame.mouse.get_pos()

        world_mouse =  self.camera.project_ground(
            Vector3(mouse_position[0], mouse_position[1], 0)
        )

        if world_mouse:
            self.mouse.position = world_mouse


    def mouse_clicked(self):
        path = self.pathfinder.find_path(self.player.position, self.mouse.position)
        if not path:
            print("No path to target")
            return
        self.player.walk_on_path(path)

            
    def update(self) -> None:
        self.input()
        for actor in self.visible_actors:
            actor.update(self.obstacles)


    def transform(self) -> None:
        for actor in self.visible_actors:
            actor.transform(self.camera)


    def draw(self) -> None:
        """Sorted acording to screen z position"""
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: actor.screen_position.z):
            actor.draw(self.display_surface)