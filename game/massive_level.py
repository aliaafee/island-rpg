import pygame
import math
import random

from .math import Vector3
from .camera import Camera
from .actors.grid import Grid
from .actors.vegetation import Tree, Palm
from .actors.grid import Grid
from .actors.box import Box
from .actors.mouse import Mouse
from .pathfinder import Pathfinder
from .actors.player import Player
from .actors.rock import Rock
from .scene import Scene
from .resources import load_map_config


class MassiveLevel:
    def __init__(self) -> None:
        self.cell_size = 10
        self.screen = pygame.display.get_surface()

        self.camera = Camera(
            position=Vector3(0, 0, 0),
            origin=Vector3(
                self.screen.get_width()/2, 
                self.screen.get_height()/2,
                0
            ),
            screen_tile_size=(64, 32),
            world_grid_size=self.cell_size
        )

        map_size = (2000000000, 2000000000)
        cell_size = 200
        cell_count= (int(map_size[0]/cell_size), int(map_size[1]/cell_size))
        
        

        self.mouse = Mouse()

        self.scene = Scene(
            size=map_size, 
            cell_count=cell_count,
            pathfinder_cell_count=(20, 20)
        )
        self.pathfinder = self.scene

        self.grid = Grid(
            cell_count=self.scene._pathfinder.grid_cell_count, 
            cell_size=self.scene._pathfinder.cell_size
        )

        self.visible_actors = []
        
        for i in range(10):
            tree = Tree(
                position=Vector3(
                    random.randint(50, 200) + 5,
                    random.randint(50, 200) + 5,
                    0
                ),
                size=Vector3(1, 1, 1)
            )
            self.scene.append(tree)

        self.player = Player(
            position=Vector3(
                2000000,
                2000000,
                0
            ),
            size=Vector3(10, 10, 10)
        )
        self.camera.position = self.player.position


    def input(self) -> None:
        world_mouse =  self.camera.project_ground(
            Vector3(*pygame.mouse.get_pos(), 0)
        )
        if world_mouse:
            self.mouse.position = world_mouse
            
        keys = pygame.key.get_pressed()


    def mouse_clicked(self, event) -> None:
        for actor in self.visible_actors:
            if self.mouse.position.distance_to(actor.base_position) < 10:
                self.player.interact_with(actor)
                return

        path = self.scene.find_path(self.player.position, self.mouse.position)
        if not path:
            print("Path not found")
            return
        
        self.player.walk_on_path(path)


    def key_pressed(self, event) -> None:
        if event.key == pygame.K_t:
            tree = Tree(
                size=Vector3(5, 5, 5)
            )
            tree.set_topleft_position(Vector3(
                math.floor(self.mouse.position.x / 10) * 10 + 5,
                math.floor(self.mouse.position.y / 10) * 10 + 5,
                0
            ))
            self.scene.append(tree)

        if event.key == pygame.K_r:
            tree = Rock(
                size=Vector3(5, 5, 5)
            )
            tree.set_topleft_position(Vector3(
                math.floor(self.mouse.position.x / 10) * 10 + 5,
                math.floor(self.mouse.position.y / 10) * 10 + 5,
                0
            ))
            self.scene.append(tree)

        if event.key == pygame.K_p:
            tree = Palm(
                size=Vector3(5, 5, 5)
            )
            tree.set_topleft_position(Vector3(
                math.floor(self.mouse.position.x / 10) * 10 + 5,
                math.floor(self.mouse.position.y / 10) * 10 + 5,
                0
            ))
            self.scene.append(tree)


    def update(self) -> None:
        self.visible_actors = self.scene.get_visible_actors(self.camera.position) + [self.player]

        self.input()

        for actor in self.visible_actors:
            actor.update(self)

        self.grid.position = Vector3(self.scene._visible_origin)
    
        self.camera.update(follow_actor=self.player)
        
        

    def transform(self) -> None:
        self.grid.transform(self.camera)
        self.mouse.transform(self.camera)
        for actor in self.visible_actors:
            actor.transform(self.camera)

        # Draw ocupied cells
        points = []
        for y, row in enumerate(self.scene._pathfinder.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    points.append(
                        Vector3(
                            x * self.scene._pathfinder.cell_size[0] + self.scene._pathfinder.cell_size[0]/2,
                            y * self.scene._pathfinder.cell_size[1] + self.scene._pathfinder.cell_size[0]/2,
                            0
                        ) + self.scene._visible_origin
                    )
        self.pf_points = [
            self.camera.transform(p)
            for p in points
        ]
        

    def draw(self) -> None:
        self.grid.draw(self.screen)
        self.mouse.draw(self.screen)
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: actor.screen_position.z):
            actor.draw(self.screen)

        for p in self.pf_points:
            pygame.draw.circle(self.screen, 'green', p.xy, 3)