import pygame

#путипутипути

#картинки данжен
CHASER_IMAGE = r'sprites\enemies\e.png'
CHASER_ATTACKING_IMAGE = r'sprites\enemies\e_atacking.png'
BOMBER_IMAGE = r'sprites\enemies\bomber.png'
BOMB_IMAGE = r'sprites\enemies\bomb.png'

BOMB_EFFECT_IMAGE = r'sprites\enemies\bomb_effect.png'

CELL_IMAGE = r'sprites\level\ph-cell.png'
WALL_IMAGE = r'sprites\level\ph-wall.png'
SHRINE_IMAGE = r'sprites\level\shrine.png'

PLAYER_IMAGE = r'sprites\player\ph-1.png'

HEART_IMAGE = r'ui\dungeon\heart.png'

#картинки ритм
TAP_IMAGE = r'sprites\player\ph-1.png'
HOLD_HEAD_IMAGE = r'sprites\player\ph-1.png'
HOLD_TAIL_IMAGE = r'sprites\rhythm\ph-hold.png'

SCORE_LINE_IMAGE = r'sprites\rhythm\ph-master-hb.png'

#музыка
TEST_MUSIC = r'test1.mp3'

#шрифты
MAIN_FONT = r'C:assets\fonts\PixelifySans-Regular.ttf'

#такты и тд
SIXTEENTH_NOTE = 1
EIGHT_NOTE = SIXTEENTH_NOTE*2
QUARTER_NOTE = EIGHT_NOTE*2
ONE_MEASURE = QUARTER_NOTE*4

#окно
SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1000

#бинды
DUNGEON_BINDS = {
    pygame.K_a : (-1, 0), 
    pygame.K_s : (0, 1),
    pygame.K_d : (1, 0),
    pygame.K_w : (0, -1),
}

RHYTM_BINDS = {
    pygame.K_a : (200, -50),
    pygame.K_s : (300, -50),
    pygame.K_d : (400, -50),
    pygame.K_f : (500, -50),
    pygame.K_g : (600, -50),
}

#евенты
SHRINE_FOUND_EVENT = pygame.event.custom_type()
GAME_OVER_EVENT = pygame.event.custom_type()