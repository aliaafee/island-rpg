
from ..resources import load_image
from .static_actor import StaticActor


class Tile(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)

        self.image_offset.y = 32

        self.show_hitbox = True

    def load_image(self, *path):
        self.set_image(load_image(*path))