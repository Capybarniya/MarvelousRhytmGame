from sprites.sprite import Sprite
from behaviors import EnemyBehavior, ChaserBehavior, BomberBehavior, BombBehavior
from utils import get_furthest_tile, get_next_step
from settings import * 

class Enemy(Sprite):
    def __init__(self, pos, sprite, groups, level_master, player):
        super().__init__(pos, sprite, groups)
        self.tile_pos = (0, 0)
        self.level_master = level_master
        self.player = player
        
        self.behavior = EnemyBehavior(self)

        self.damage = 1
        self.speed = QUARTER_NOTE
        self.hp = 1

        self.is_alive = True
        self.is_atacking = False

    def move(self, flee=False):
        if flee:
            goal = get_furthest_tile(self.player.tile_pos, ver_func = self.level_master.is_tile_movable)
        else:
            goal = self.player.tile_pos

        if self.tile_pos == goal:
            return False
        
        next_step = get_next_step(start=self.tile_pos, goal=goal, ver_func = self.level_master.is_tile_movable, max_depth=1e20)
        
        if next_step and self.level_master.is_tile_movable(next_step, check_for_enemies=True):
            self.tile_pos = (next_step[0], next_step[1])
            self.rect.center = self.level_master.get_pos_from_tile(self.tile_pos)
            return True
        
        self.tile_pos = self.level_master.get_random_tile(self.tile_pos, check_for_movable = True)

        return False
    
    def update(self, current_beat):
        if self.is_alive and current_beat % self.speed == 0:
            self.behavior.apply_next_action()
    
    def kill(self):
        super().kill()
        self.is_alive = False

class Chaser(Enemy):
    def __init__(self, pos, assets, groups, level_master, player):
        self.idle_sprite = assets.get_image(CHASER_IMAGE)
        self.attacking_sprite = assets.get_image(CHASER_ATTACKING_IMAGE)
        super().__init__(pos, self.idle_sprite, groups, level_master, player)
        self.behavior = ChaserBehavior(self)
        self.speed = QUARTER_NOTE * 2
        self.hp = 1
        
        self.duel_cooldown = 0 

    def start_duel(self):
        self.is_atacking = True
        self.image = self.attacking_sprite

    def end_duel(self):
        self.is_atacking = False
        self.image = self.idle_sprite
        self.duel_cooldown = QUARTER_NOTE*2
        self.move(flee=True)

    def update(self, current_beat):
        if self.is_alive and current_beat % self.speed == 0:
            if self.duel_cooldown > 0:
                self.duel_cooldown -= 1
            self.behavior.apply_next_action()
        
class Bomber(Enemy):
    def __init__(self, pos, assets, groups, level_master, player):
        self.idle_sprite = assets.get_image(BOMBER_IMAGE)
        super().__init__(pos, self.idle_sprite, groups, level_master, player)
        self.bomb_cooldown = 0
        self.behavior = BomberBehavior(self)
        self.speed = QUARTER_NOTE
    
    def create_bomb(self):
        self.level_master.create_bomb(self.tile_pos)
        self.bomb_cooldown = QUARTER_NOTE*8

class Bomb(Enemy):
    def __init__(self, pos, assets, groups, level_master, player, effect_spawner):
        self.idle_sprite = assets.get_image(BOMB_IMAGE)
        super().__init__(pos, self.idle_sprite, groups, level_master, player)
        self.timer = 4*2
        self.behavior = BombBehavior(self)
        self.effect_spawner = effect_spawner

    def explode(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                tile_pos = (self.tile_pos[0] + i, self.tile_pos[1] + j)
                if self.level_master.is_tile_movable(tile_pos):
                    self.effect_spawner.spawn_bomb_effect(self.level_master.get_pos_from_tile(tile_pos))
                if self.level_master.is_occupied_by_player(tile_pos):
                    self.player.hp -= self.damage
        self.kill()