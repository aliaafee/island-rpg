

class StateMachine:
    def __init__(self) -> None:
        self.handlers = {}
        self.current_state = None
        pass


    def add_state(self, name: str, handler):
        name = name.upper()
        self.handlers[name] = handler


    def set_start(self, name):
        self.current_state = name.upper()


    def set_current_state(self, name):
        self.current_state = name.upper()


    def update(self, *params) -> None:
        if not self.current_state in self.handlers.keys():
            return

        handler = self.handlers[self.current_state]

        self.set_current_state(handler(*params))
