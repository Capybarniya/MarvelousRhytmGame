from ui.health_bar import HealthBar
from ui.minimap import MiniMap
from ui.timer import Timer
from settings import *  
from utils import coords_sum

class UIRhythm():
    def __init__(self, assets, score_master):
        self.score_master = score_master
        self.font_score = pygame.font.Font(MAIN_FONT, 26)
        self.font_mod = pygame.font.Font(MAIN_FONT, 40)
        self.font_grade = pygame.font.Font(MAIN_FONT, 40)
        self.color_nums = (42, 42, 42)
        self.color_grade = (42, 42, 42)

    def draw(self, screen):
        score = str(self.score_master.score)
        modifier = str(self.score_master.combo_modifier)
        grade = str(self.score_master.last_grade)

        score_sur = self.font_score.render(score, True, self.color_nums)
        screen.blit(score_sur, (18, 810))

        modifier_sur = self.font_mod.render('x'+modifier , True, self.color_nums)
        screen.blit(modifier_sur, (18, 760))

        grade_sur = self.font_grade.render(grade , True, self.color_grade)
        screen.blit(grade_sur, (18, 667))