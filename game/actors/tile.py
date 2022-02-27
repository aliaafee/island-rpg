
from ..resources import load_image
from .static_actor import StaticActor


class Tile(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.set_image(
            load_image(
                "tiles",
                "ts_grass0",
                "straight",
                "45",
                "0.png"
            )
        )
        self.image_offset.y = 32

        self.show_hitbox = True

    def load_image(self, *path):
        self.set_image(load_image(*path))