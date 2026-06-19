import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite
        self.rect = self.image.get_frect(center=pos)