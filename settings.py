import pygame

#путипутипути

#картинки данжен
BACKGROUND_DUNGEON_IMAGE = r'backgrounds\dungeon_backrgound.png'
BACKGROUND_UPPER_DUNGEON_IMAGE = r'backgrounds\dungeon_backrgound_b.png'

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

HINT_DUNGEON = r'ui\hints\hint_dungeon.png'

#картинки ритм
BACKGROUND_RHYTHM_IMAGE = r'backgrounds\rhythm_backrgound.png'
BACKGROUND_UPPER_RHYTHM_IMAGE = r'backgrounds\rhythm_backrgound_b.png'

HIT_IDLE_IMAGE = r'sprites\rhythm\tester_idle.png'
HIT_HIT_IMAGE = r'sprites\rhythm\tester_happy.png'
HIT_MISS_IMAGE = r'sprites\rhythm\tester_angry.png'

TAP_IMAGE = r'sprites\rhythm\tap_head.png'
HOLD_HEAD_IMAGE = r'sprites\rhythm\hold_head.png'
HOLD_TAIL_IMAGE = r'sprites\rhythm\ph-hold.png'

SCORE_LINE_IMAGE = r'sprites\rhythm\ph-master-hb.png'

HINT_RHYTHM = r'ui\hints\hint_rhythm.png'

#музыка
TEST_MUSIC = r'test1.mp3'
DUNGEON_MUSIC = r'04.30 ! syn_6.mp3'
RHYTHM_MUSIC = r'04.30 ! syn_fin.mp3'

#шрифты
MAIN_FONT = r'assets\fonts\PixelCode\PixelCode-Black.otf'

#такты и тд
SIXTEENTH_NOTE = 0.5
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
    pygame.K_a : (300, -50),
    pygame.K_s : (400, -50),
    pygame.K_d : (500, -50),
    pygame.K_f : (600, -50),
    pygame.K_g : (700, -50),
}

#евенты
SHRINE_FOUND_EVENT = pygame.event.custom_type()
GAME_OVER_EVENT = pygame.event.custom_type()
VICTORY_EVENT = pygame.event.custom_type()