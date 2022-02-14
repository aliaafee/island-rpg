import pygame
import math
from .actor import Actor
from .player import Player
from .vegetation import Tree
from .mouse import Mouse
from .math import Vector3, Vector2
from .camera import Camera
from .debug import debug

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []
        self.obstacles = []

        self.load_level()


    def load_level(self) -> None:
        self.camera = Camera(
            position=Vector3(0, 0, 0),
            origin=Vector3(
                self.display_surface.get_width()/2, 
                self.display_surface.get_height()/2,
                0
            ),
            rotation_deg=45,
            tilt_deg=60
        )
        

        self.player = Player([self.visible_actors])
        self.player.position = Vector3(100, 100, 0)

        self.obstacle = Tree([self.visible_actors, self.obstacles])
        self.obstacle.position = Vector3(150, -100, 0)

        self.tree = Tree([self.visible_actors, self.obstacles])
        self.tree.position = Vector3(-150, 0, 0)

        self.mouse = Mouse([self.visible_actors])


    def input(self) -> None:
        keys = pygame.key.get_pressed()

        pan = Vector3(0,0,0)
        if keys[pygame.K_UP]:
            pan.y += 1
        elif keys[pygame.K_DOWN]:
            pan.y -= 1
        elif keys[pygame.K_LEFT]:
            pan.x += 1
        elif keys[pygame.K_RIGHT]:
            pan.x -= 1
        self.camera.position = self.camera.position + pan


        mouse_position = pygame.mouse.get_pos()

        world_mouse =  self.camera.project_ground(
            Vector3(mouse_position[0], mouse_position[1], 0)
        )

        if world_mouse:
            self.mouse.position = world_mouse
        
        mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
        if mouse1:
            debug("{}, {}".format(mouse_position, self.mouse.position))
            self.player.walk_to(self.mouse.position)
            

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