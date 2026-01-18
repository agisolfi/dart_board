class Screen:
    def __init__(self, screen):
        self.screen = screen
        self._next = None

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def next_screen(self):
        return self._next
