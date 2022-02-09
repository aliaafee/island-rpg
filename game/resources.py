import pygame
import os

RES_ROOT = "."
GFX_ROOT = os.path.join(RES_ROOT, "graphics")

def load_image(*path: str) -> pygame.surface.Surface:
    return pygame.image.load(os.path.join(GFX_ROOT, *path)).convert_alpha()
