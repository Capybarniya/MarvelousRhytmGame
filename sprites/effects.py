from sprites.sprite import Sprite
from settings import *

class Effect(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.duration = 4

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()

class EffectSpawner():
    def __init__(self, assets, all_sprites_group, effect_sprites_group):
        self.bomb_effect_image = assets.get_image(BOMB_EFFECT_IMAGE)
        self.all_sprites = all_sprites_group
        self.effect_sprites = effect_sprites_group

    def spawn_bomb_effect(self, pos):
        Effect(pos, self.bomb_effect_image, (self.all_sprites, self.effect_sprites))