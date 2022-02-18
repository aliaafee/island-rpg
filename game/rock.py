from .resources import load_image
from .math import Vector3
from .static_actor import StaticActor


class Rock(StaticActor):
    def __init__(self, groups=...) -> None:
        super().__init__(groups)
        self.set_image(load_image("test", "rock.png"))
        self.image_offset.y = +10

        self.set_hitbox(Vector3(30, 30, 50))
        self.show_hitbox = True