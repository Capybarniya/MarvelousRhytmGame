import pygame
from game_mods.game_state import GameState
from game_mods.paused_state import PausedState
from game_mods.dungeon_mode import DungeonMode
from game_mods.rhythm_mode import RhythmMode
from game_mods.game_over_state import GameOverState
from game_mods.victory_state import VictoryState
from game_mods.hint_state import HintState
from settings import * 

class PlayingState(GameState):
    def enter(self):
        pygame.mixer.music.unpause()
        self.state_machine.mode_machine.set_mode(DungeonMode)
    
    def exit(self):
        pygame.mixer.music.stop()
        self.game.level_master.cleanup()
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def resume(self):
        pygame.mixer.music.unpause()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_machine.push_state(PausedState)
                return
            if event.key == pygame.K_F1:
                self.state_machine.mode_machine.set_mode(RhythmMode)
                return
        if event.type == SHRINE_FOUND_EVENT:
            self.state_machine.mode_machine.set_mode(RhythmMode)
            self.state_machine.push_state(HintState, (HINT_RHYTHM))
            return
        if event.type == GAME_OVER_EVENT:
            self.state_machine.push_state(GameOverState)
            return
        if event.type == VICTORY_EVENT:
            self.state_machine.push_state(VictoryState, (event.score))
            return
        
        self.state_machine.mode_machine.handle_event(event)
    
    def update(self, dt):
        self.state_machine.mode_machine.update(dt)
    
    def render(self, screen):
        self.state_machine.mode_machine.render(screen)
    
