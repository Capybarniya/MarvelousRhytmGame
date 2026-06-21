import pygame

from ui.ui_component import UIComponent
from utils import coords_sum
from settings import * 

class Timer(UIComponent):
    def __init__(self, origin_pos, assets, music_master):
        super().__init__(origin_pos, assets)
        self.music_master = music_master
        self.font_big = pygame.font.Font(MAIN_FONT, 60)
        self.font_small = pygame.font.Font(MAIN_FONT, 24)

    def draw(self, screen):
        time = self.music_master.get_time_left()
        if time >= 10:
            color = (180, 177, 182)
        else:
            color = (255, 0, 0)
        time = str(float(time))
        big_time, small_time = time.split('.')
        small_time = small_time[:3]
        score_big = self.font_big.render(big_time+'.', True, color)
        score_small = self.font_small.render(small_time, True, color)
        screen.blit(score_big, self.origin_pos)
        screen.blit(score_small, coords_sum(self.origin_pos, (score_big.get_width(), 16)))