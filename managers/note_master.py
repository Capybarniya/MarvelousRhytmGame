import pygame
from sprites import Sprite, TapNote, HoldNote, HitEffect
from playlist import PLAYLIST_1
from settings import *

class NoteMaster:
    ORIGINS = list(RHYTM_BINDS.values())
    ORIGINS_BINDS = list(RHYTM_BINDS.keys())

    def __init__(self, game_mode, music_master, score_master, note_sprites, assets):
        self.game = game_mode
        
        self.music_master = music_master
        self.score_master = score_master
        self.assets = assets
        
        self.notes = note_sprites

        self.playlist = PLAYLIST_1
        self.current_line = 0
        self.next_line_time = 0

        self.key_cooldowns = {k: 0.0 for k in self.ORIGINS_BINDS}
        self.input_cooldown = 0.25

        self.score_line = pygame.Rect(0, 815, 1000, 1)
        self.miss_line = pygame.Rect(0, 900, 1000, 1)

        self.hit_effects = pygame.sprite.Group()
        self.hit_effects_list = []
        
        for x, _ in self.ORIGINS:
            effect = HitEffect((x, self.score_line.centery), self.assets, self.hit_effects)
            self.hit_effects_list.append(effect)

    def handle_input(self, key):
        current_time = self.music_master.current_song_time
        if current_time < self.key_cooldowns[key]:
            return

        origin_idx = self.ORIGINS_BINDS.index(key)
        target_y = self.score_line.top
        closest_proj = None
        min_dist = float('inf')

        for proj in self.notes.sprites():
            if proj.origin == origin_idx and type(proj) == TapNote:
                dist = abs(proj.hitbox_rect.centery - target_y)

                hit_windows = [grade['hit_window'] for grade in self.game.score_master.GRADES if grade['hit_window'] != float('inf')]
                hit_window = max(hit_windows)

                if dist < min_dist and dist <= hit_window:
                    min_dist = dist
                    closest_proj = proj

            if proj.origin == origin_idx and type(proj) == HoldNote:
                for i, tail in enumerate(proj.tails):
                    if i == len(proj.tails) - 1: last_tail = tail
                dist = abs(last_tail.rect.centery - target_y)

                hit_windows = [grade['hit_window'] for grade in self.game.score_master.GRADES if grade['hit_window'] != float('inf')]
                hit_window = max(hit_windows)

                if dist < min_dist and dist <= hit_window:
                    min_dist = dist
                    closest_proj = proj

        if closest_proj:
            if type(closest_proj) == TapNote: 
                closest_proj.kill()
            
            self.game.score_master.judge(min_dist)
            
            self.hit_effects_list[origin_idx].trigger('hit')

        self.key_cooldowns[key] = current_time + self.input_cooldown

    def update(self):
        self._update_beats()
        self._check_states()
        
        self.hit_effects.update()

    def _update_beats(self):
        while self.music_master.current_song_time >= self.next_line_time:
            self._spawn_current_beat()
            beat_count, _ = self.playlist[self.current_line]
            self.next_line_time += beat_count * self.music_master.beat_duration
            self.current_line += 1

    def _spawn_current_beat(self):
        _, lanes = self.playlist[self.current_line]
        current_time = self.music_master.current_song_time
        for i, active in enumerate(lanes):
            if active:
                if active < 0:
                    self._spawn_HoldNote(i, current_time, abs(active))
                else:
                    self._spawn_TapNote(i, current_time)

    def _spawn_TapNote(self, origin, current_time):
        TapNote(self, origin, self.assets, self.notes, current_time)

    def _spawn_HoldNote(self, origin, current_time, duration):
        HoldNote(self, origin, self.assets, self.notes, current_time, duration, self.game.tail_sprites)

    def _check_states(self):
        self._check_holds()
        self._check_misses()

    def _check_misses(self):
        for note in self.notes.sprites():
            if type(note) == TapNote:
                if note.hitbox_rect.bottom > self.miss_line.top:
                    note.kill()
                    self.score_master.judge('miss')
                    
                    self.hit_effects_list[note.origin].trigger('miss')
                    
            elif type(note) == HoldNote:
                for i, tail in enumerate(note.tails):
                    if tail.rect.bottom > self.miss_line.top and tail.is_active:
                        self.score_master.judge('miss')
                        tail.is_active = False
                        
                        self.hit_effects_list[note.origin].trigger('miss')
                        
                    if i == len(note.tails) - 1 and tail.rect.top > self.miss_line.top:
                        note.kill()

    def _check_holds(self):
        keys = pygame.key.get_pressed()
        for note in self.notes.sprites():
            if type(note) == HoldNote:
                for i, tail in enumerate(note.tails): 
                    if tail.rect.bottom > self.miss_line.top and tail.is_active and keys[self.ORIGINS_BINDS[note.origin]]:
                        self.score_master.judge('hold')
                        tail.is_active = False