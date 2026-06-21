from sprites.sprite import Sprite
import pygame
from settings import * 

class Note(Sprite):
    def __init__(self, master, origin, sprite, groups, origin_time):
        super().__init__(master.ORIGINS[origin], sprite, groups)
        self.origin = origin
        self.master = master
        self.origin_time = origin_time
        self.hitbox_rect = self.rect.inflate(80, 80)

    def move_head(self):
        TRACK_LENGTH = 8
        BEAT_DURATION = self.master.music_master.beat_duration
        TRACK_DURATION = BEAT_DURATION * TRACK_LENGTH
        TRACK_HEIGHT = 900

        current_time = pygame.mixer.music.get_pos() / 1000.0
        time_since_origin = current_time - self.origin_time
        progress = time_since_origin / TRACK_DURATION

        start_y = -50
        end_y = TRACK_HEIGHT - self.hitbox_rect.height
        self.hitbox_rect.y = start_y + progress * (end_y - start_y)
        self.rect.center = self.hitbox_rect.center

        self._move_tail()

    def _move_tail(self):
        pass

class TapNote(Note):
    def __init__(self, master, origin, assets, groups, origin_time):
        self.idle_img = assets.get_image(TAP_IMAGE)
        super().__init__(master, origin, self.idle_img, groups, origin_time)

class Tail(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.is_active = True

class HoldNote(Note):
    distance_per_beat = 900 / 8
    distance_per_16 = distance_per_beat/4
    
    def __init__(self, master, origin, assets, head_groups, origin_time, duration, tail_groups):
        self.idle_img = assets.get_image(HOLD_HEAD_IMAGE)
        super().__init__(master, origin, self.idle_img, head_groups, origin_time)
        tail_sprite = assets.get_image(HOLD_TAIL_IMAGE)
        tail_sprite = pygame.transform.scale(tail_sprite, (64, self.distance_per_16))
        self.tails = [Tail((self.rect.centerx, self.rect.centery - i * self.distance_per_16), tail_sprite , tail_groups) for i in range(duration*4)]
    
    def _move_tail(self):
        for i, tail in enumerate(self.tails):
            tail.rect.center = (self.rect.centerx, self.rect.centery - i * self.distance_per_16)

    def kill(self):
        super().kill()
        for tail in self.tails: tail.kill()
