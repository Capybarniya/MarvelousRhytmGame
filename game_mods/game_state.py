class GameState():
    def __init__(self, game, state_machine):
        self.game = game
        self.state_machine = state_machine
    
    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def pause(self):
        pass
    
    def resume(self):
        pass
    
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        pass