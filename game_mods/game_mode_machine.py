class GameModeMachine:
    def __init__(self, game):
        self.game = game
        self.current_mode = None
            
    def set_mode(self, mode_class):
        if self.current_mode:
            self.current_mode.exit()
        
        self.current_mode = mode_class(self.game)
        self.current_mode.enter()
    
    def handle_event(self, event):
        if self.current_mode:
            self.current_mode.handle_event(event)
    
    def update(self, dt):
        if self.current_mode:
            self.current_mode.update(dt)
    
    def render(self, screen):
        if self.current_mode:
            self.current_mode.render(screen)