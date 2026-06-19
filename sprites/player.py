import pygame
from sprites.sprite import Sprite
from utils import tools
from settings import * 

class Player(Sprite):
    BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w]

    def __init__(self, pos, assets, groups, level_master):
        self.idle_image = assets.get_image(PLAYER_IMAGE)
        super().__init__(pos, self.idle_image, groups)
        self.tile_pos = (2, 2)
        self.level_master = level_master
        self.hp = 3

        self.is_atacked = False

    def handle_input(self, key):
        if key == pygame.K_a:
            dir = (-1, 0)
        if key == pygame.K_s:
            dir = (0, 1)
        if key == pygame.K_d:
            dir = (1, 0)
        if key == pygame.K_w:
            dir = (0, -1)

        if self.is_atacked:
            atacker = None
            for enemy in self.level_master.game.enemy_sprites:
                if enemy.is_atacking:
                    atacker = enemy
                    break
            
            if atacker is not None:
                atack_dir = tools.coords_sum((-1*self.tile_pos[0], -1*self.tile_pos[1]), atacker.tile_pos)
                if atack_dir == dir:
                    atacker.hp -= 1
                    if atacker.hp <= 0:
                        atacker.kill()
                        self.is_atacked = False
                else:
                    self.hp -= 1
            else:
                self.is_atacked = False
        else:
            new_tile_pos = tools.coords_sum(dir, self.tile_pos)
            enemy = self.level_master.is_occupied_by_enemy(new_tile_pos)
            if enemy:
                pass
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.kill()
            else:
                door = self.level_master.get_door(new_tile_pos)
                if door: 
                    #print(self.level_master.current_room_coords + dir)
                    self.level_master.change_room(tools.coords_sum(self.level_master.current_room_coords, dir))
                    self.tile_pos = self.level_master.get_pair_pos_from_door(door)
                    print(self.tile_pos)
                elif self.level_master.is_tile_movable(new_tile_pos): 
                    self.tile_pos = new_tile_pos

                self.rect.center = self.level_master.get_pos_from_tile(self.tile_pos)