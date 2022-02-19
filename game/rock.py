from .resources import load_image
from .math import Vector3
from .static_actor import StaticActor


class Rock(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        self.set_image(load_image("test", "rock.png"))
        self.image_offset.y = +10
