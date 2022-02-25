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


test_map = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 7, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 6, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [5, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#test_map = [
#    [ 1 for x in range(100)] for y in range(100)
#]

test_grid_size = 10


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []
        self.obstacles = []
        self.interactive = []

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
            world_grid_size=test_grid_size
        )

        for y, row in enumerate(test_map):
            for x, cell in enumerate(row):
                if cell == 0:
                    box = Box(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(test_grid_size, test_grid_size, test_grid_size)
                    )
                    box.set_topleft_position(Vector3(x * test_grid_size , y * test_grid_size , 0))
                if cell == 5:
                    rock = Rock(
                        groups=[self.visible_actors, self.obstacles, self.interactive],
                        size=Vector3(test_grid_size, test_grid_size, test_grid_size)
                    )
                    rock.set_topleft_position(Vector3(x * test_grid_size , y * test_grid_size , 0))
                if cell == 6:
                    tree = Palm(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(test_grid_size, test_grid_size, test_grid_size)
                    )
                    tree.set_topleft_position(Vector3(x * test_grid_size , y * test_grid_size , 0))
                if cell == 7:
                    tree = Tree(
                        groups=[self.visible_actors, self.obstacles],
                        size=Vector3(test_grid_size, test_grid_size, test_grid_size)
                    )
                    tree.set_topleft_position(Vector3(x * test_grid_size , y * test_grid_size , 0))

        self.player = Player(groups=[self.visible_actors])
        self.player.position = Vector3(test_grid_size * 2, test_grid_size, 0)

        self.mouse = Mouse(groups=[self.visible_actors])

        grid_size = (len(test_map[0]), len(test_map))
        self.grid = Grid(groups=[self.visible_actors], size=grid_size)

        self.pathfinder = Pathfinder((test_grid_size * grid_size[0], test_grid_size * grid_size[1]), grid_size)
        self.pathfinder.add_obstacles(
            [(o.position, o.size) for o in self.obstacles]
        )


    def input(self) -> None:
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

            
    def update(self) -> None:
        self.input()
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