import pygame
from game_mods.game_mod import GameMode

from managers import MusicMaster, NoteMaster, ScoreMaster

class RhythmMode(GameMode):
    def __init__(self, game):
        super().__init__(game)
        self.note_sprites = pygame.sprite.Group()
        self.tail_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        self.music_master = MusicMaster(self.game.asset_master)
        self.score_master = ScoreMaster()
        self.note_master = NoteMaster(self, self.music_master, self.score_master, self.note_sprites, self.game.asset_master)
        
    
    def enter(self):
        pygame.mixer.music.play()

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in self.note_master.ORIGINS_BINDS:
                self.note_master.handle_input(event.key)
    
    def update(self, dt):
        for note in self.note_sprites.sprites():
                note.move_head()
        self.music_master.update()
        self.note_master.update()
    
    def render(self, screen):
        self.background_sprites.draw(screen)
        self.tail_sprites.draw(screen)
        self.note_sprites.draw(screen)
        self.score_master.draw_score(screen)