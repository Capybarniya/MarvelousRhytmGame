import pygame
from game_mods.game_state import GameState

class GameOverState(GameState):
    def enter(self):
        self.pause_alpha = 128
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                from game_mods.playing_state import PlayingState
                self.state_machine.change_state(PlayingState)
                return
            
            if event.key == pygame.K_q:
                self.state_machine.change_state(GameState)
                return

    def render(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.pause_alpha))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        
        hint_font = pygame.font.Font(None, 36)
        hint = hint_font.render("R - Retry | Q - Quit to Menu", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(hint, hint_rect)