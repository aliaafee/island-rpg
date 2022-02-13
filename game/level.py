import pygame
import math
from .actor import Actor
from .player import Player
from .vegetation import Tree
from .mouse import Mouse
from .math import Transformation, Matrix3x3, Vector3, Vector2
from .debug import debug

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_actors = []
        self.obstacles = []

        self.load_level()
        


    def load_level(self) -> None:
        alpha = (45/180) * math.pi
        beta = (60/180) * math.pi

        self.transformation = Transformation(
            Matrix3x3([
                [                 math.sin(alpha),             -1 * math.sin(alpha),                   0],
                [math.cos(beta) * math.sin(alpha), math.cos(beta) * math.cos(alpha), -1 * math.sin(beta)],
                [math.sin(beta) * math.sin(alpha), math.sin(beta) * math.cos(alpha),      math.cos(beta)]
            ]),
            Vector3(
                self.display_surface.get_width()/2, 
                self.display_surface.get_height()/2,
                0
            )
        )

        #Used for converting screen coordinates to coordinates on the ground plane
        self.screen_x_axis = self.transformation._inverse_transformation * Vector3(1, 0, 0)
        self.screen_y_axis = self.transformation._inverse_transformation * Vector3(0, 1, 0)
        self.screen_y_axis.z = 0
        t_x_axis = self.transformation.transform(self.screen_x_axis).x - self.transformation.translation.x
        t_y_axis = self.transformation.transform(self.screen_y_axis).y - self.transformation.translation.y
        self.screen_y_axis = self.screen_y_axis * t_x_axis/t_y_axis
        

        self.player = Player([self.visible_actors])
        self.player.position = Vector3(100, 100, 0)
        #self.player.show_hotbox = True

        self.obstacle = Tree([self.visible_actors, self.obstacles])
        self.obstacle.position = Vector3(150, -100, 0)

        self.tree = Tree([self.visible_actors, self.obstacles])
        self.tree.position = Vector3(-150, 0, 0)

        self.mouse = Mouse([self.visible_actors])


    def to_ground_position(self, screen_position: Vector2) -> Vector3:
        screen_position3 = Vector3(screen_position.x, screen_position.y, 0) - self.transformation.translation
        
        #"""
        t_orig = self.transformation.transform(Vector3(0,0,0))
        t_x_axis = self.transformation.transform(self.screen_x_axis * 100)
        t_y_axis = self.transformation.transform(self.screen_y_axis* 100)

        pygame.draw.circle(self.display_surface, 'grey', t_orig.xy, 3)
        pygame.draw.circle(self.display_surface, 'blue', t_x_axis.xy, 3)
        pygame.draw.circle(self.display_surface, 'green', t_y_axis.xy, 3)
        #"""

        return (self.screen_x_axis * screen_position3.x) + (self.screen_y_axis * screen_position3.y)



    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.transformation.translation.y += 1
        elif keys[pygame.K_DOWN]:
            self.transformation.translation.y -= 1
        elif keys[pygame.K_LEFT]:
            self.transformation.translation.x += 1
        elif keys[pygame.K_RIGHT]:
            self.transformation.translation.x -= 1


        mouse_position = pygame.mouse.get_pos()

        self.mouse.position = self.to_ground_position(Vector2(pygame.mouse.get_pos()))
        
        mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
        if mouse1:
            debug("{}, {}".format(mouse_position, self.mouse.position))
            self.player.position = self.mouse.position


            

    def update(self) -> None:
        self.input()
        for actor in self.visible_actors:
            actor.update(self.obstacles)

    def transform(self) -> None:
        for actor in self.visible_actors:
            actor.transform(self.transformation)#, self.translation)

    def draw(self) -> None:
        """Sorted according to distance between point and the line x + y = 0 on the ground plane"""
        
        for actor in sorted(self.visible_actors, 
                            key = lambda actor: (actor.position.x + actor.position.y) / 1.4142135623730951):
            actor.draw(self.display_surface)