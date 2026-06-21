import pygame
from game_mods.game_state import GameState
from sprites import Sprite
from settings import *

class HintState(GameState):
    def __init__(self, game, state_machine, hint_image):
        super().__init__(game, state_machine)
        hint_image = self.assets.get_image(hint_image)
        self.hints = pygame.sprite.Group()
        self.hint = Sprite((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), hint_image, self.hints)
        
    def enter(self):
        self.pause_alpha = 172
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.state_machine.pop_state()
            return
            
    def render(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.pause_alpha))
        screen.blit(overlay, (0, 0))

        self.hints.draw(screen)
        
        