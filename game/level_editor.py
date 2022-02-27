import pygame
import math

from .math import Vector3
from .camera import Camera
from .actors.grid import Grid
from .actors.mouse import Mouse
from .actors.tile import Tile
from .actors.ground import Ground
from .resources import get_image_filenames


class LevelEditor:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.cell_count = (10, 10)
        self.cell_size = 10
        self.ui_group = []

        self.tile_names = get_image_filenames("tiles")
        self.tile_varients = get_image_filenames("tiles", self.tile_names[0])
        self.tile_angles = get_image_filenames("tiles", self.tile_names[0], self.tile_varients[0])

        self.tile_name_i = 0
        self.tile_varient_i = 0
        self.tile_angle_i = 0

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

        self.grid = Grid(groups=[self.ui_group], cell_count=self.cell_count, cell_size=self.cell_size)
        self.ground = Ground(groups=[self.ui_group], cell_count=self.cell_count, cell_size=self.cell_size)
        self.mouse = Mouse(groups=[self.ui_group])
        self.cursor_tile = Tile(groups=[self.ui_group])


    def toggle_cursor_tile(self, dir=1):
        self.tile_name_i = self.tile_name_i + dir
        if self.tile_name_i > len(self.tile_names) - 1 : self.tile_name_i = 0
        if self.tile_name_i < 0 : self.tile_name_i = len(self.tile_names) - 1
        
        self.tile_varients = get_image_filenames("tiles", self.tile_names[self.tile_name_i])
        self.tile_varient_i = 0
        self.tile_angles = get_image_filenames("tiles", self.tile_names[self.tile_name_i], self.tile_varients[self.tile_varient_i])
        self.tile_angle_i = 0
        self.cursor_tile.load_image(
            "tiles",
            self.tile_names[self.tile_name_i],
            self.tile_varients[self.tile_varient_i],
            self.tile_angles[self.tile_angle_i],
            "0.png"
        )


    def toggle_cursor_variants(self, dir=1):
        self.tile_varient_i = self.tile_varient_i + dir
        if self.tile_varient_i > len(self.tile_varients) - 1 : self.tile_varient_i = 0
        if self.tile_varient_i < 0 : self.tile_varient_i = len(self.tile_varients) - 1
        
        self.tile_angles = get_image_filenames("tiles", self.tile_names[self.tile_name_i], self.tile_varients[self.tile_varient_i])
        self.tile_angle_i = 0

        self.cursor_tile.load_image(
            "tiles",
            self.tile_names[self.tile_name_i],
            self.tile_varients[self.tile_varient_i],
            self.tile_angles[self.tile_angle_i],
            "0.png"
        )


    def input(self):
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


    def mouse_clicked(self, event):
        if event.button == pygame.BUTTON_LEFT:
            self.ground.set_cell_image(
                self.mouse.position,
                self.cursor_tile.image
            )
        
        if event.button == pygame.BUTTON_WHEELUP:
            self.toggle_cursor_tile()
        if event.button == pygame.BUTTON_WHEELDOWN:
            self.toggle_cursor_variants()

    def update(self) -> None:
        self.input()
        self.cursor_tile.set_topleft_position(
            Vector3(
                math.floor(self.mouse.position.x / 10) * 10,
                math.floor(self.mouse.position.y / 10) * 10,
                0
            )
        )


    def transform(self) -> None:
        for actor in self.ui_group:
            actor.transform(self.camera)


    def draw(self) -> None:
        for actor in self.ui_group:
            actor.draw(self.display_surface)