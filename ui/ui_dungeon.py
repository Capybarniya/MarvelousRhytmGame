from ui.health_bar import HealthBar
from ui.minimap import MiniMap
from ui.timer import Timer
from settings import *  
from utils import coords_sum

class UIDungeon():
    def __init__(self, level_master, assets, music_master):
        self.components = []

        origin_health_bar = (SCREEN_WIDTH-64*3-32, 64)
        self.components.append(HealthBar(origin_health_bar, assets, level_master.player))
        
        origin_minimap = (32, 32)
        self.components.append(MiniMap(origin_minimap, assets, level_master))

        origin_timer = coords_sum((SCREEN_WIDTH//2, 0), (-64, 16))
        self.components.append(Timer(origin_timer, assets, music_master))

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)