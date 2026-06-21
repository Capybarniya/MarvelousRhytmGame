import pygame
from game_mods.game_state import GameState

class PausedState(GameState):
    def enter(self):
        self.pause_alpha = 128
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_machine.pop_state()
                return
            
            if event.key == pygame.K_q:
                from game_mods.main_menu_state import MainMenuState
                self.state_machine.change_state(MainMenuState)
                return

    def render(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.pause_alpha))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        
        hint_font = pygame.font.Font(None, 36)
        hint = hint_font.render("ESC - Resume | Q - Quit to Menu", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(hint, hint_rect)