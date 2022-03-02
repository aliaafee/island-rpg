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




class Scene:
    def __init__(self, size=(1000, 1000), cell_count=(10, 10), pathfinder_cell_count=(100, 100)) -> None:
        self.width, self.height = size
        self.cells_x, self.cells_y = cell_count
        self._grid = {}
        self._visible_cells = {}
        self._visible_actors = []
        self._visible_origin = None
        self._visible_end = None

        self._pathfinder = Pathfinder(
            grid_size=(self.width / self.cells_x * 3, self.height / self.cells_y * 3),
            cell_count=pathfinder_cell_count
        )
        print("Path finder cell size = {}".format(self._pathfinder.cell_size))

    def _get_cell_id(self, point):
        x, y = point
        if x < 0 or y < 0:
            return None
        if x > self.width or y > self.width:
            return None
        return (
            math.floor(x / self.width * self.cells_x),
            math.floor(y / self.height * self.cells_y)
        )

    def _is_valid_cell(self, x, y):
        if x < 0:
            return False
        if y < 0:
            return False
        if x > self.cells_x - 1:
            return False
        if y > self.cells_y - 1:
            return False
        return True

    def _get_cell_ids_including_adjacent(self, point):
        cell = self._get_cell_id(point)
        if not cell:
            return None
        yield cell
        cx, cy = cell
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x or y:
                    ax, ay = cx + x, cy + y
                    if self._is_valid_cell(ax, ay):
                        yield (ax, ay)


    def _get_actors_in_cell(self, cell_id):
        if not cell_id in self._grid:
            return []
        return self._grid[cell_id]

    
    def append(self, actor) -> bool:
        location = self._get_cell_id(actor.position.xy)

        if not location:
            return False

        if not location in self._grid:
            self._grid[location] = []

        self._grid[location].append(actor)

        if location in self._visible_cells:
            print("Updated the visible cells")
            self._visible_cells[location] = self._grid[location]


    def get_visible_actors(self, position: Vector3):
        current_cells = list(self._get_cell_ids_including_adjacent(position.xy))
        
        new_visible_cells = {}
        for cell_id in self._visible_cells:
            if cell_id in current_cells:
                new_visible_cells[cell_id] = self._visible_cells[cell_id]

        i = 0
        for cell_id in current_cells:
            if not cell_id in new_visible_cells:
                i += 1
                new_visible_cells[cell_id] = self._get_actors_in_cell(cell_id)
        if i > 0:
            print("Loaded: {} cells".format(i))
        self._visible_cells = new_visible_cells

        if not self._visible_cells:
            self._visible_actors = []
            self._visible_origin = None
            self._visible_end = None
            self._pathfinder.clear()
            return []

        self._visible_actors = []
        for actors in self._visible_cells.values():
            self._visible_actors.extend(actors)

        min_cell_id = min(self._visible_cells.keys())
        
        self._visible_origin = Vector3(
            self.width / self.cells_x * min_cell_id[0],
            self.height / self.cells_y * min_cell_id[1],
            0
        )

        max_cell_id = max(self._visible_cells.keys())

        self._visible_end = Vector3(
            self.width / self.cells_x * (max_cell_id[0] + 1),
            self.height / self.cells_y * (max_cell_id[1] + 1),
            0
        )
        
        self._pathfinder.clear()
        self._pathfinder.add_obstacles([
            (actor.position - self._visible_origin, actor.size)
            for actor in self._visible_actors
        ])
        
        return self._visible_actors


    def is_valid_point(self, point: Vector3):
        if self._visible_end == None or self._visible_origin == None:
            return False
        if point.x < self._visible_origin.x or point.x > self._visible_end.x:
            return False
        if point.y < self._visible_origin.y or point.y > self._visible_end.y:
            return False
        return True


    def find_path(self, start: Vector3, end: Vector3, diagonal=True):
        if not self.is_valid_point(start):
            return None
        if not self.is_valid_point(end):
            return None

        path = self._pathfinder.find_path(
            start - self._visible_origin, 
            end - self._visible_origin, 
            diagonal
        )

        if not path:
            return None
        
        return [
            node + self._visible_origin
            for node in path
        ]
        
        

    

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
        cell_count=(int(map_size[0]/cell_size), int(map_size[1]/cell_size))

        self.mouse = Mouse()

        self.scene = Scene(
            size=map_size, 
            cell_count=cell_count,
            pathfinder_cell_count=(60, 60)
        )
        self.pathfinder = self.scene

        self.grid = Grid(
            cell_count=self.scene._pathfinder.grid_cell_count, 
            cell_size=self.scene._pathfinder.cell_size[0]
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