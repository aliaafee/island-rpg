import pygame
import math

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from .actor import Actor
from .player import Player
from .vegetation import Tree
from .rock import Rock
from .mouse import Mouse
from .math import Vector3, Vector2
from .camera import Camera
from .debug import debug

test_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
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
                    rock = Rock([self.visible_actors, self.obstacles])
                    rock.position = Vector3(x*test_grid_size, y*test_grid_size, 0)
        
        self.grid = Grid(matrix=test_map)

        self.player = Player([self.visible_actors])
        self.player.position = Vector3(0, 0, 0)

        self.mouse = Mouse([self.visible_actors])


    def to_grid_node(self, point: Vector3, grid: Grid):
        x = int((point.x + (test_grid_size/2)) / test_grid_size)
        y = int((point.y + (test_grid_size/2)) / test_grid_size)
        if not grid.inside(x,y):
            return None
        print(x,y)
        return grid.node(x, y)


    def find_path(self, startv: Vector3, endv: Vector3):
        #grid = Grid(matrix=test_map)
        self.grid.cleanup()
        
        start = self.to_grid_node(startv, self.grid)
        end = self.to_grid_node(endv, self.grid)
        
        if not(start and end):
            return None
        
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        
        path, runs = finder.find_path(start, end, self.grid)

        if not path:
            return None
        
        walk_points = [Vector3(x * test_grid_size, y * test_grid_size, 0) for (x, y) in path[1:]]

        #print('operations:', runs, 'path length:', len(path))
        #print(grid.grid_str(path=path, start=start, end=end))

        return walk_points


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
        travel_path = self.find_path(self.player.position, self.mouse.position)
        if not travel_path:
            return
        self.player.walk_on_path(travel_path)
                   
            
    def update(self) -> None:
        self.input()
        for actor in self.visible_actors:
            actor.update(self.obstacles)
        #self.camera.position = self.player.position


    def transform(self) -> None:
        for actor in self.visible_actors:
            actor.transform(self.camera)


    def draw(self) -> None:
        """Sorted acording to screen z position"""
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: actor.screen_position.z):
            actor.draw(self.display_surface)