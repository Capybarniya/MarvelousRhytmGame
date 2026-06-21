import pygame
from settings import *

class MusicMaster:
    def __init__(self, assets):
        self.assets = assets

        self.bpm = 104
        self.beat_duration = 60 / (self.bpm*QUARTER_NOTE)
        self.song_duration = 30
        self.current_beat = 0
        self.next_beat_time = 0
        self.hit_window = 0.15
        self.current_song_time = 0
        self.last_beat_processed = -1

    def is_time_on_beat(self):
        time_to_beat = (self.current_song_time+0.5) % self.beat_duration*QUARTER_NOTE
        return min(time_to_beat, self.beat_duration*QUARTER_NOTE - time_to_beat) <= self.hit_window
    
    def is_new_beat(self):
        if self.current_beat > self.last_beat_processed:
            self.last_beat_processed = self.current_beat
            return True
        return False
    
    def update(self):
        self.current_song_time = pygame.mixer.music.get_pos() / 1000.0
        self._check_game_over()
        while self.current_song_time >= self.next_beat_time:
            self.next_beat_time += self.beat_duration
            self.current_beat += 1

    def start_music(self):
        pygame.mixer.music.load(self.assets.get_music_path(TEST_MUSIC))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def _check_game_over(self):
        if self.current_song_time > self.song_duration:
            exit_event = pygame.event.Event(GAME_OVER_EVENT)
            pygame.event.post(exit_event)

    def get_time_left(self):
        return self.song_duration - self.current_song_time
