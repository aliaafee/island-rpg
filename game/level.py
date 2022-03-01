import random
import pygame

from .actors.player import Player
from .actors.vegetation import Tree, Palm
from .actors.rock import Rock
from .actors.mouse import Mouse
from .math import Vector3
from .camera import Camera
from .debug import debug
from .pathfinder import Pathfinder
from .actors.box import Box
from .actors.grid import Grid


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []
        self.obstacles = []
        self.interactive = []
        self.cell_size = 10

        self.load_level()


    def load_level(self) -> None:
        self.camera = Camera(
            position=Vector3(0, 0, 0),
            origin=Vector3(
                self.display_surface.get_width()/2, 
                self.display_surface.get_height()/2,
                0
            ),
            screen_tile_size=(64, 32),
            world_grid_size=self.cell_size
        )

        map = self.generate_random_map((100, 100), player_cell=(50, 50))

        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == 0:
                    box = Box(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(self.cell_size, self.cell_size, self.cell_size)
                    )
                    box.set_topleft_position(Vector3(x * self.cell_size , y * self.cell_size , 0))
                if cell == 5:
                    rock = Rock(
                        groups=[self.visible_actors, self.obstacles, self.interactive],
                        size=Vector3(self.cell_size, self.cell_size, self.cell_size)
                    )
                    rock.set_topleft_position(Vector3(x * self.cell_size , y * self.cell_size , 0))
                if cell == 6:
                    tree = Palm(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(self.cell_size, self.cell_size, self.cell_size)
                    )
                    tree.set_topleft_position(Vector3(x * self.cell_size , y * self.cell_size , 0))
                if cell == 7:
                    tree = Tree(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(self.cell_size, self.cell_size, self.cell_size)
                    )
                    tree.set_topleft_position(Vector3(x * self.cell_size , y * self.cell_size , 0))

        self.player = Player(
            groups=[self.visible_actors],
            size=Vector3(*[self.cell_size]*3)
        )
        self.player.set_topleft_position(Vector3(50 * self.cell_size, 50 * self.cell_size, 0))
        self.camera.position = Vector3(self.player.position)

        self.mouse = Mouse(groups=[self.visible_actors])

        cell_count = (len(map[0]), len(map))
        self.grid = Grid(groups=[self.visible_actors], cell_count=cell_count, cell_size=self.cell_size)

        self.pathfinder = Pathfinder((self.cell_size * cell_count[0], self.cell_size * cell_count[1]), cell_count)
        self.pathfinder.add_obstacles(
            [(o.position, o.size) for o in self.obstacles]
        )


    def generate_random_map(self, size, player_cell=(0, 0)):
        width, height = size
        
        map = [
            [1 for x in range(width)] for y in range (height)
        ]

        for i in range(300):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if x != player_cell[0] and y != player_cell[1]:
                map[y][x] = random.choice([6, 7])
        
        x = player_cell[0] - 5
        y = player_cell[1]
        map[y][x] = 5

        x = player_cell[0] + 5
        y = player_cell[1]
        map[y][x] = 5

        
        return map


    def input(self) -> None:
        keys = pygame.key.get_pressed()

        # pan = Vector3(0,0,0)
        # if keys[pygame.K_UP]:
        #     pan.y -= 4
        # elif keys[pygame.K_DOWN]:
        #     pan.y += 4
        # elif keys[pygame.K_LEFT]:
        #     pan.x -= 4
        # elif keys[pygame.K_RIGHT]:
        #     pan.x += 4
        # if pan.length_squared != 0:
        #     self.camera.pan(pan)

        mouse_position = pygame.mouse.get_pos()

        world_mouse =  self.camera.project_ground(
            Vector3(mouse_position[0], mouse_position[1], 0)
        )

        if world_mouse:
            self.mouse.position = world_mouse


    def mouse_clicked(self, event):
        for actor in self.interactive:
            if self.mouse.position.distance_to(actor.base_position) < 10:
                self.player.interact_with(actor)
                return

        path = self.pathfinder.find_path(self.player.position, self.mouse.position)

        if not path:
            print("No path to target")
            return
        self.player.walk_on_path(path)


    def key_pressed(self, event):
        print(event)

            
    def update(self) -> None:
        self.input()
        self.camera.update(follow_actor=self.player)
        for actor in self.visible_actors:
            actor.update(self)


    def transform(self) -> None:
        for actor in self.visible_actors:
            actor.transform(self.camera)


    def draw(self) -> None:
        """Sorted acording to screen z position"""
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: actor.screen_position.z):
            actor.draw(self.display_surface)