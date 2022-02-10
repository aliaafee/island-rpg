import pygame
import os

RES_ROOT = "."
GFX_ROOT = os.path.join(RES_ROOT, "graphics")

def load_image(*path: str) -> pygame.surface.Surface:
    return pygame.image.load(os.path.join(GFX_ROOT, *path)).convert_alpha()


def load_image_folder(*path: str) -> list:
    image_list = []
    foldername = os.path.join(GFX_ROOT, *path)
    for _,_,image_filenames in os.walk(foldername):
        for image_filename in sorted(image_filenames):
            image = pygame.image.load(os.path.join(foldername, image_filename)).convert_alpha()
            image_list.append(image)
    return image_list