import pygame
import os
import json

resources_cache = {}

RES_ROOT = "."
GFX_ROOT = os.path.join(RES_ROOT, "graphics")
MAPS_ROOT = os.path.join(RES_ROOT, "maps")


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


def get_image_filenames(*path: str) -> list:
    foldername = os.path.join(GFX_ROOT, *path)
    return os.listdir(foldername)


def load_map_config(map_name) -> dict:
    with open(os.path.join(MAPS_ROOT, map_name, 'config.json')) as f:
        data = json.load(f)
    return data