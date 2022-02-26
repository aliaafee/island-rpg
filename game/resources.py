import pygame
import os

resources_cache = {}

RES_ROOT = "."
GFX_ROOT = os.path.join(RES_ROOT, "graphics")


def _load_image(path: str) -> pygame.surface.Surface:
    global resources_cache
    if not path in resources_cache:
        resources_cache[path] = pygame.image.load(path).convert_alpha()
    return resources_cache[path]


def load_image(*path: str) -> pygame.surface.Surface:
    return _load_image(os.path.join(GFX_ROOT, *path))


def load_image_folder(*path: str) -> list:
    image_list = []
    foldername = os.path.join(GFX_ROOT, *path)
    for _,_,image_filenames in os.walk(foldername):
        for image_filename in sorted(image_filenames):
            image = _load_image(os.path.join(foldername, image_filename))
            image_list.append(image)
    return image_list