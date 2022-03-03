import pygame
import math
import random

from .math import Vector3
from .camera import Camera
from .resources import load_map_config
from .pathfinder import Pathfinder
from .actors.grid import Grid
from .actors.mouse import Mouse
from .actors.player import Player
from .actors.vegetation import Tree, Palm


class WorldCell:
    def __init__(self, cell_id: tuple, cell_size: tuple) -> None:
        self.cell_id = cell_id
        self.cell_size = cell_size
        self.position = Vector3(
            cell_id[0] * cell_size[0],
            cell_id[1] * cell_size[1],
            0
        )
        self._actors = []
        self.placeholder = Grid(
            position=self.position,
            cell_count=(1, 1),
            cell_size=cell_size,
            color='red'
        )
        self.loaded = False
        self.load()


    def load(self):
        print("Loading {}".format(self))
        random.seed(self.cell_id[0] + self.cell_id[1])
        for i in range(random.randint(0, 5)):
            tree = Tree(
                position=Vector3(
                    random.randint(0, self.cell_size[0]),
                    random.randint(0, self.cell_size[1]),
                    0
                ) + self.position,
                size=Vector3(1, 1, 1)
            )
            self._actors.append(tree)
        for i in range(random.randint(0, 5)):
            tree = Palm(
                position=Vector3(
                    random.randint(0, self.cell_size[0]),
                    random.randint(0, self.cell_size[1]),
                    0
                ) + self.position,
                size=Vector3(1, 1, 1)
            )
            self._actors.append(tree)
        self.loaded = True


    @property
    def actors(self) -> list:
        if not self.loaded:
            return [self.placeholder]

        return self._actors


    def __repr__(self) -> str:
        return str(self.cell_id)


class World:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.map_name = "world"
        self.load()


    def load(self):
        self.map_config = load_map_config(self.map_name)

        self.width, self.height = self.map_config['map_size']
        #self.width, self.height = (100, 100)

        self.cells_x, self.cells_y = self.map_config['cell_count']
        #self.cells_x, self.cells_y = (10, 10)

        self.pf_cells_x, self.pf_cells_y = self.map_config['pathfinder_cell_count']
        #self.pf_cells_x, self.pf_cells_y = (2, 2)

        self.cell_width, self.cell_height = (
            self.width / self.cells_x,
            self.height / self.cells_y
        )

        self.camera = Camera(
            position=Vector3(0, 0, 0),
            origin=Vector3(
                self.screen.get_width()/2, 
                self.screen.get_height()/2,
                0
            ),
            screen_tile_size=self.map_config['tile_size']
        )

        #Pathfinding works on the center cell and 8 adjacet cells
        self.pathfinder = Pathfinder(
            grid_size=(self.cell_width * 3, self.cell_height * 3),
            cell_count=(
                self.pf_cells_x * 3,
                self.pf_cells_y * 3,
            )
        )

        #Grid for visualizing the pathfinder space
        self.pathfinder_grid = Grid(
            cell_count=self.pathfinder.grid_cell_count,
            cell_size=self.pathfinder.cell_size
        )

        #Mouse cursor
        self.mouse = Mouse()

        #The visible cells
        self.visible_cells = {}

        #start and end of visible region
        self.visible_origin = None
        self.visible_end = None

        #the player
        self.player = Player(
            position = Vector3(20, 20, 0)
        )
        self.camera.position = self.player.position


    def position_to_cell_id(self, position: Vector3) -> tuple:
        if position.x < 0 or position.y < 0:
            return None
        if position.x > self.width or position.y > self.height:
            return None
        return (
            math.floor(position.x / self.width * self.cells_x),
            math.floor(position.y / self.height * self.cells_y)
        )


    def is_valid_cell(self, x, y):
        if x < 0:
            return False
        if y < 0:
            return False
        if x > self.cells_x - 1:
            return False
        if y > self.cells_y - 1:
            return False
        return True


    def visible_cell_ids(self, center: Vector3):
        center_cell = self.position_to_cell_id(center)
        if not center_cell: 
            return []
        cells = []
        cx, cy = center_cell
        for y in range(-1, 2):
            for x in range(-1, 2):
                ix, iy = x + cx, y + cy
                if self.is_valid_cell(ix, iy):
                    cells.append((ix, iy))
        return cells


    def update_visible_cells(self, center: Vector3):
        current_cells = self.visible_cell_ids(center)
        
        new_visible_cells = {}
        
        for cell_id in self.visible_cells:
            if cell_id in current_cells:
                new_visible_cells[cell_id] = self.visible_cells[cell_id]

        i = 0
        for cell_id in current_cells:
            if not cell_id in new_visible_cells:
                i += 1
                new_visible_cells[cell_id] = WorldCell(
                    cell_id=cell_id,
                    cell_size=(self.cell_width, self.cell_height)
                )
        if i > 0: print("Loaded: {} cells".format(i))

        self.visible_cells = new_visible_cells

        if not self.visible_cells:
            self.visible_origin = None
            self.visible_end = None
            return

        min_active = min(self.visible_cells.keys())
        self.visible_origin = Vector3(
            self.width / self.cells_x * min_active[0],
            self.height / self.cells_y * min_active[1],
            0
        )

        max_active = max(self.visible_cells.keys())
        self.visible_end = Vector3(
            self.width / self.cells_x * (max_active[0] + 1),
            self.height / self.cells_y * (max_active[1] + 1),
            0
        )

        self.pathfinder.clear()
        self.pathfinder.position = self.visible_origin
        for cell in self.visible_cells.values():
            self.pathfinder.add_obstacles([
                (actor.position, actor.size)
                for actor in cell.actors
            ])


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
        path = self.pathfinder.find_path(self.player.position, self.mouse.position)
        if not path:
            print("Path not found")
            return
        
        self.player.walk_on_path(path)


    def key_pressed(self, event) -> None:
        pass


    def update(self) -> None:
        self.input()

        self.update_visible_cells(self.camera.position)

        self.active_actors = [self.player]
        for cell in self.visible_cells.values():
            self.active_actors.extend(cell.actors)

        for actor in self.active_actors:
            actor.update(self)

        self.camera.update(follow_actor=self.player)



    def transform(self) -> None:
        self.mouse.transform(self.camera)

        for actor in self.active_actors:
            actor.transform(self.camera)

    
    def draw(self) -> None:
        self.draw_debug()

        self.mouse.draw(self.screen)

        for actor in sorted(self.active_actors, 
                            key = lambda actor: actor.screen_position.z):
            actor.draw(self.screen)


    def draw_debug(self):
        if not self.visible_origin is None:
            self.pathfinder_grid.position = self.visible_origin
            self.pathfinder_grid.cell_count = (
                math.floor((self.visible_end.x - self.visible_origin.x) / self.cell_width) * self.pf_cells_x,
                math.floor((self.visible_end.y - self.visible_origin.y) / self.cell_height) * self.pf_cells_y
            )
            self.pathfinder_grid.transform(self.camera)

        if not self.visible_origin is None:
            self.pathfinder_grid.draw(self.screen)