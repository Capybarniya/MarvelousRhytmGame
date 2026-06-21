
import pygame
from sprites import Sprite
from settings import *

class HitEffect(Sprite):
    def __init__(self, pos, assets, groups):
        self.assets = assets
        self.images = {
            'idle': assets.get_image(HIT_IDLE_IMAGE),
            'hit': assets.get_image(HIT_HIT_IMAGE),
            'miss': assets.get_image(HIT_MISS_IMAGE)
        }
        print(pos)
        super().__init__(pos, self.images['idle'], groups)
        
        self.state = 'idle'
        
        self.timer = 0
        self.duration = 1000

    def trigger(self, state):
        if state in self.images:
            self.state = state
            self.image = self.images[state]
            self.timer = pygame.time.get_ticks() + self.duration

    def update(self):
        if self.timer > 0 and pygame.time.get_ticks() > self.timer:
            self.state = 'idle'
            self.image = self.images['idle']
            self.timer = 0