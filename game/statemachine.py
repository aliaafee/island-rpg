

class StateMachine:
    def __init__(self, start) -> None:
        self.handlers = {}
        self.first_run_current_state = True
        self.set_start(start)


    def add_state(self, name: str, handler):
        name = name.upper()
        self.handlers[name] = handler


    def set_start(self, name):
        self.current_state = name.upper()


    def set_current_state(self, name):
        next_state = name.upper()
        
        if next_state != self.current_state:
            self.first_run_current_state = True

        self.current_state = name.upper()


    def update(self, *params) -> None:
        if not self.current_state in self.handlers.keys():
            return

        handler = self.handlers[self.current_state]

        if self.first_run_current_state:
            self.first_run_current_state = False
            self.set_current_state(handler(*params, first_run=True))
            return

        self.set_current_state(handler(*params, first_run=False))
