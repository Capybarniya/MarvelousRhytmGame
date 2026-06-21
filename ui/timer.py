import pygame

from ui.ui_component import UIComponent
from utils import coords_sum
from settings import * 

class Timer(UIComponent):
    def __init__(self, origin_pos, assets, music_master):
        super().__init__(origin_pos, assets)
        self.music_master = music_master

    def draw(self, screen):
        font_big = pygame.font.Font(MAIN_FONT, 64)
        font_small = pygame.font.Font(MAIN_FONT, 32)
        time = self.music_master.get_time_left()
        if time >= 10:
            color = (0, 0, 0)
        else:
            color = (255, 0, 0)
        time = str(time)
        big_time, small_time = time.split('.')
        small_time = small_time[:3]
        score_big = font_big.render(big_time+'.', True, color)
        score_small = font_small.render(small_time, True, color)
        screen.blit(score_big, self.origin_pos)
        screen.blit(score_small, coords_sum(self.origin_pos, (score_big.get_width(), 16)))