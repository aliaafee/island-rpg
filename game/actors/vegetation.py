import random
from ..resources import load_image
from ..math import Vector3
from .static_actor import StaticActor


class Tree(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.set_image(load_image("vegetation", "tree0{}.png".format(random.randint(1, 4))))
        self.image_offset.y = 60

        self.show_hitbox = True




class Palm(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        
        self.set_image(load_image("vegetation", "palm0{}.png".format(random.randint(1, 4))))
        self.image_offset.y = 15

        self.show_hitbox = True