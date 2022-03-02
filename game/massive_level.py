import pygame
import math
import random

from .math import Vector3
from .camera import Camera
from .actors.grid import Grid
from .actors.vegetation import Tree, Palm
from .actors.grid import Grid
from .actors.mouse import Mouse




class Scene:
    def __init__(self, size=(100, 100), cell_count=(2, 2)) -> None:
        self.width, self.height = size
        self.cells_x, self.cells_y = cell_count
        self._grid = {}
        self._visible_cells = {}
        self._visible_actors = []

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


    def get_visible_actors(self, position: Vector3):
        current_cells = list(self._get_cell_ids_including_adjacent(position.xy))
        
        obsolete_ids = []
        for cell_id in self._visible_cells:
            if not cell_id in current_cells:
                obsolete_ids.append(cell_id)
        
        for obsolete_id in obsolete_ids:
            self._visible_cells.pop(obsolete_id)

        i = 0
        for cell_id in current_cells:
            if not cell_id in self._visible_cells:
                i += 1
                self._visible_cells[cell_id] = self._get_actors_in_cell(cell_id)
        if i > 0:
            print("Loaded: {} cells".format(i))
        
        self._visible_actors = []
        for actors in self._visible_cells.values():
            self._visible_actors.extend(actors)
        
        return self._visible_actors
        

    

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

        map_size = (2000, 2000)
        cell_size = 200
        cell_count=(int(map_size[0]/cell_size), int(map_size[1]/cell_size))

        self.grid = Grid(
            cell_count=cell_count, 
            cell_size=cell_size
        )
        self.mouse = Mouse()

        self.scene = Scene(size=map_size, cell_count=cell_count)

        self.visible_actors = []
        
        for i in range(1000):
            tree = Tree(
                position=Vector3(
                    random.randint(0, map_size[0]),
                    random.randint(0, map_size[1]),
                    0
                ),
                size=Vector3(0, 0, 0)
            )
            self.scene.append(tree)


    def input(self) -> None:
        world_mouse =  self.camera.project_ground(
            Vector3(*pygame.mouse.get_pos(), 0)
        )
        if world_mouse:
            self.mouse.position = world_mouse
            
        keys = pygame.key.get_pressed()

        pan = Vector3(0,0,0)
        if keys[pygame.K_UP]:
            pan.y -= 4
        elif keys[pygame.K_DOWN]:
            pan.y += 4
        elif keys[pygame.K_LEFT]:
            pan.x -= 4
        elif keys[pygame.K_RIGHT]:
            pan.x += 4
        if pan.length_squared != 0:
            self.camera.pan(pan)

    def mouse_clicked(self, event) -> None:
        tree = Palm(
            position=Vector3(self.mouse.position),
            size=Vector3(0, 0, 0)
        )
        self.scene.append(tree)


    def key_pressed(self, event) -> None:
        if event.key == pygame.K_a:
            tree = Palm(
                position=Vector3(self.mouse.position),
                groups=[self.visible_actors],
                size=Vector3(0, 0, 0)
            )
            self.scene.append(tree)


    def update(self) -> None:
        self.input()

        #self.visible_actors = [a for a in self.scene.get_actors(self.mouse.position.xy)]
        #self.scene.set_visible_position(self.mouse.position.xy)
        self.visible_actors = self.scene.get_visible_actors(self.camera.position)
        

    def transform(self) -> None:
        self.grid.transform(self.camera)
        self.mouse.transform(self.camera)
        for actor in self.visible_actors:
            actor.transform(self.camera)
        

    def draw(self) -> None:
        self.grid.draw(self.screen)
        self.mouse.draw(self.screen)
        i = 0
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: actor.screen_position.z):
            i += 1
            actor.draw(self.screen)
        print(i)