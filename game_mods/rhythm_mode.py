import pygame
from game_mods.game_mod import GameMode

from sprites import Sprite
from managers import MusicMaster, NoteMaster, ScoreMaster
from ui import UIRhythm
from settings import *
from utils import coords_sum 

class RhythmMode(GameMode):
    def __init__(self, game):
        super().__init__(game)
        self.note_sprites = pygame.sprite.Group()
        self.tail_sprites = pygame.sprite.Group()

        self.background_sprites = pygame.sprite.Group()
        self.background_upper_sprites = pygame.sprite.Group()

        background_img = self.game.asset_master.get_image(BACKGROUND_RHYTHM_IMAGE)
        Sprite((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), background_img, self.background_sprites)

        background_upper_img = self.game.asset_master.get_image(BACKGROUND_UPPER_RHYTHM_IMAGE)
        Sprite(coords_sum((261, 814), (background_upper_img.get_width()//2 + 2, background_upper_img.get_height()//2)), background_upper_img, self.background_upper_sprites)

        self.music_master = MusicMaster(self.game.asset_master)
        self.score_master = ScoreMaster()
        self.note_master = NoteMaster(self, self.music_master, self.score_master, self.note_sprites, self.game.asset_master)

        self.music_master.set_song_duration(60+57)

        self.ui = UIRhythm(self.game.asset_master, self.score_master)
        
    
    def enter(self):
        self.music_master.start_music(RHYTHM_MUSIC)

    def exit(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            if event.key in self.note_master.ORIGINS_BINDS:
                self.note_master.handle_input(event.key)
    
    def update(self, dt):
        for note in self.note_sprites.sprites():
                note.move_head()
        self.music_master.update()
        self.note_master.update()
        if self.music_master.check_if_time_over():
            exit_event = pygame.event.Event(VICTORY_EVENT, {'score': self.score_master.score})
            pygame.event.post(exit_event)
    
    def render(self, screen):
        self.background_sprites.draw(screen)
        self.tail_sprites.draw(screen)
        self.note_sprites.draw(screen)
        self.background_upper_sprites.draw(screen)
        self.note_master.hit_effects.draw(screen)
        self.ui.draw(screen)