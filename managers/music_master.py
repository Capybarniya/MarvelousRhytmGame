import pygame
from settings import *

class MusicMaster:
    def __init__(self, game):
        self.game = game

        self.bpm = 104
        self.beat_duration = 60 / (self.bpm*QUARTER_NOTE)
        self.current_beat = 0
        self.next_beat_time = 0
        self.hit_window = 0.15

        pygame.mixer.music.load(self.game.asset_master.get_music_path(TEST_MUSIC))
        pygame.mixer.music.set_volume(0.5)

    def is_time_on_beat(self, current_time):
        time_to_beat = (current_time+0.5) % self.beat_duration*QUARTER_NOTE
        return min(time_to_beat, self.beat_duration*QUARTER_NOTE - time_to_beat) <= self.hit_window
    
    def update_beats(self, current_song_time):
        while current_song_time >= self.next_beat_time:
            self.next_beat_time += self.beat_duration
            self.current_beat += 1
            #print(current_song_time)