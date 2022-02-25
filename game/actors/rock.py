from ..resources import load_image
from ..math import Vector3
from ..statemachine import StateMachine
from .static_actor import StaticActor



class Rock(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        self.set_image(load_image("test", "rock.png"))
        self.image_offset.y = +10

        self.statemachine = StateMachine()
        self.statemachine.set_start("idle")
        self.statemachine.add_state("idle", self.idle_state)

        self.rising = False
        self.elevating_actor = None
        self.statemachine.add_state("rising", self.rising_state)


    def is_elevated(self):
        return self.position.z > 5


    def idle_state(self, level, first_run=False):
        if self.rising and self.elevating_actor:
            return "rising"

        return "idle"


    def rising_state(self, level, first_run=False):
        self.position.z += 0.5
        self.elevating_actor.position.z += 0.5

        if self.is_elevated():
            self.rising = False
            self.elevating_actor = None
            return "idle"

        return "rising"


    def interact(self, actor):
        if self.is_elevated():
            return True
        self.rising = True
        self.elevating_actor = actor
        return None


    def update(self, level) -> None:
        super().update(level)

        self.statemachine.update(level)
