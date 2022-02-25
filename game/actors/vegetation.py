from ..resources import load_image
from ..math import Vector3
from .static_actor import StaticActor


class Tree(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.set_image(load_image("vegetation", "tree01.png"))
        self.image_offset.y = 60

        self.show_hitbox = True




class Palm(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.set_image(load_image("vegetation", "palm03.png"))
        self.image_offset.y = 15

        self.show_hitbox = True