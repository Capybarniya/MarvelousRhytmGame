import pygame
from sprites.sprite import Sprite
from sprites.enemies import Chaser
from settings import * 

class Player(Sprite):
    BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w]

    def __init__(self, pos, assets, groups, level_master):
        self.idle_image = assets.get_image(PLAYER_IMAGE)
        super().__init__(pos, self.idle_image, groups)
        self.tile_pos = (2, 2)
        self.level_master = level_master
        self.hp = 3

        self.locked_by = None
        self.parry_attempted = False
        self.lock_start_beat = -1
    def update(self, current_beat):
        self._check_game_over()
        self._check_missed_parry(current_beat)
        self._check_lock(current_beat)
        
    def _check_lock(self, current_beat):
        if self.locked_by: 
            return

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            check_pos = (self.tile_pos[0] + dx, self.tile_pos[1] + dy)
            enemy = self.level_master.is_occupied_by_enemy(check_pos)
            
            if enemy and hasattr(enemy, 'start_duel') and enemy.duel_cooldown == 0:
                self.locked_by = enemy
                enemy.start_duel()
                self.lock_start_beat = current_beat
                break
    
    def _check_game_over(self):
        if self.hp <= 0:
            exit_event = pygame.event.Event(GAME_OVER_EVENT)
            pygame.event.post(exit_event)

    def attempt_parry(self, dir):
        if not self.locked_by:
            return
            
        self.parry_attempted = True

        chaser_pos = self.locked_by.tile_pos
        dir_to_chaser = (chaser_pos[0] - self.tile_pos[0], chaser_pos[1] - self.tile_pos[1])

        if dir == dir_to_chaser:
            self.locked_by.hp -= 1
            if self.locked_by.hp <= 0:
                self.locked_by.kill()
            self.resolve_lock()
        else:
            self.resolve_lock(player_takes_damage=True)

    def resolve_lock(self, player_takes_damage=False):
        if self.locked_by:
            if self.locked_by.is_alive:
                self.locked_by.end_duel()
            self.locked_by = None
            
        if player_takes_damage:
            self.hp -= 1
            
        self.parry_attempted = False
        self.lock_start_beat = -1

    def _check_missed_parry(self, current_beat):
        if not self.locked_by:
            return
            
        if current_beat >= self.lock_start_beat + 2:
            if not self.parry_attempted:
                self.resolve_lock(player_takes_damage=True)

    def move(self, dir):
        if self.locked_by:
            return

        new_tile_pos = (self.tile_pos[0] + dir[0], self.tile_pos[1] + dir[1])
        
        if self.level_master.is_occupied_by_enemy(new_tile_pos):
            return 
        
        self.level_master.check_for_shrine(new_tile_pos)
            
        door = self.level_master.get_door(new_tile_pos)
        if door: 
            self.level_master.change_room(
                (self.level_master.current_room_coords[0] + dir[0], self.level_master.current_room_coords[1] + dir[1])
            )
            self.tile_pos = self.level_master.get_pair_pos_from_door(door)
        elif self.level_master.is_tile_movable(new_tile_pos): 
            self.tile_pos = new_tile_pos

        self.rect.center = self.level_master.get_pos_from_tile(self.tile_pos)