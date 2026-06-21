import pygame
from game_mods.game_state import GameState
from game_mods.main_menu_state import MainMenuState

class VictoryState(GameState):
    def __init__(self, game, state_machine, score):
        super().__init__(game, state_machine)
        self.score = score

    def enter(self):
        self.pause_alpha = 128
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                from game_mods.playing_state import PlayingState
                self.state_machine.change_state(PlayingState)
                return
            
            if event.key == pygame.K_q:
                self.state_machine.change_state(MainMenuState)
                return

    def render(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.pause_alpha))
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("YOU WON", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)

        hint_font = pygame.font.Font(None, 36)
        hint = hint_font.render(f"Your Score - {self.score}", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(hint, hint_rect)
        
        hint_font = pygame.font.Font(None, 36)
        hint = hint_font.render("R - Play Again | Q - Quit to Menu", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 120))
        screen.blit(hint, hint_rect)