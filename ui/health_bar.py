import pygame
from sprites import Sprite
from settings import *
from utils import coords_sum
from ui.ui_component import UIComponent

class HealthBar(UIComponent):
    def __init__(self, origin_pos, assets, player,):
        super().__init__(origin_pos, assets)
        self.player = player

    def draw(self, screen):
        hp = self.player.hp
        self.sprites = pygame.sprite.Group()
        heart_image = self.assets.get_image(HEART_IMAGE)
        for i in range(hp):
            Sprite(coords_sum(self.origin_pos, (64*i, 0)), heart_image, self.sprites)
        self.sprites.draw(screen)

        