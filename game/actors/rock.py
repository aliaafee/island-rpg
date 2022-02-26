from re import T
from game.pathfinder import F
from ..resources import load_image
from ..math import Vector3
from ..statemachine import StateMachine
from .static_actor import StaticActor



class Rock(StaticActor):
    def __init__(self, **kargs) -> None:
        super().__init__(**kargs)
        self.set_image(load_image("test", "rock.png"))
        self.image_offset.y = +10

        self.busy = False

        self.statemachine = StateMachine("idle")
        self.statemachine.add_state("idle", self.idle_state)

        self.rising = False
        self.statemachine.add_state("rising", self.rising_state)

        self.depressing = False
        self.statemachine.add_state("depressing", self.depressing_state)


    def is_elevated(self):
        return self.position.z > 10


    def is_depressed(self):
        return self.position.z < 1


    def idle_state(self, level, first_run=False):
        if self.rising:
            return "rising"

        if self.depressing:
            return "depressing"

        return "idle"


    def rising_state(self, level, first_run=False):
        if first_run:
            print("Start Elevating")

        self.position.z += 0.2

        if self.is_elevated():
            self.rising = False
            self.busy = False
            return "idle"

        return "rising"


    def depressing_state(self, level, first_run=False):
        if first_run:
            print("Start Depressing")

        self.position.z -= 0.2

        if self.is_depressed():
            self.depressing = False
            self.busy = False
            return "idle"

        return "depressing"


    def start_interaction(self, actor) -> None:
        if self.is_depressed():
            self.rising = True
            self.busy = True
        if self.is_elevated():
            self.depressing = True
            self.busy = True


    def interaction_completed(self) -> bool:
        """
        Prevents actor from interacting with other actors
        """
        return not self.busy


    def update(self, level) -> None:
        super().update(level)

        self.statemachine.update(level)
