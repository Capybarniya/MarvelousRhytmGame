from game_mods.game_mode_machine import GameModeMachine

class GameStateMachine:
    def __init__(self, game):
        self.game = game
        self.mode_machine = GameModeMachine(game)
        self._stack = []
    
    @property
    def current_state(self):
        return self._stack[-1] if self._stack else None
    
    def push_state(self, state_class, *args, **kwargs):

        if self.current_state:
            self.current_state.pause()
        
        state = state_class(self.game, self, *args, **kwargs)
        self._stack.append(state)
        state.enter()
    
    def pop_state(self):
        if self._stack:
            old_state = self._stack.pop()
            old_state.exit()
            
            if self.current_state:
                self.current_state.resume()
    
    def change_state(self, state_class, *args, **kwargs):
        if self._stack:
            old_state = self._stack.pop()
            old_state.exit()
        
        state = state_class(self.game, self, *args, **kwargs)
        self._stack.append(state)
        state.enter()
    
    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)
    
    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self, screen):
        for state in self._stack:
            state.render(screen)