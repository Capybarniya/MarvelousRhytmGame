import random

import pygame

import tools
from level_generator import*

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite
        self.rect = self.image.get_frect(center=pos)

class Tile(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.is_movable = True

class Wall(Tile):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.is_movable = False

class Cell(Tile):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class Door(Tile):
    def __init__(self, pos, sprite, groups, direction):
        super().__init__(pos, sprite, groups)
        self.direction = direction 

class EnemyBehavior:
    def __init__(self, enemy):
        self.enemy = enemy

    def get_next_action(self):
        pass

class ChaserBehavior(EnemyBehavior):
    def __init__(self, enemy):
        super().__init__(enemy)

    def get_next_action(self):
        if self.enemy.level_master.heuristic(self.enemy.tile_pos, self.enemy.player.tile_pos) <= 1:
            if not self.enemy.player.is_atacked:
                self.enemy.atack()
            else:
                pass
        else:
            self.enemy.move()

class BomberBehavior(EnemyBehavior):
    def __init__(self, enemy):
        super().__init__(enemy)

    def get_next_action(self):
        if self.enemy.bomb_cooldown == 0:
            if self.enemy.level_master.heuristic(self.enemy.tile_pos, self.enemy.player.tile_pos) < 3:
                self.enemy.create_bomb()
                self.enemy.move(flee=True)
                self.enemy.speed = 2
                #print(id(self.enemy), "bomb")
            else:
                self.enemy.speed = 4
                self.enemy.move()
                #print(id(self.enemy), "chase")
        else:
            self.enemy.speed = 8
            self.enemy.move(flee=True)
            self.enemy.bomb_cooldown -= 1
            #print(id(self.enemy), "flee")

class BombBehavior(EnemyBehavior):
    def __init__(self, enemy):
        super().__init__(enemy)

    def get_next_action(self):
        if self.enemy.timer == 0:
            self.enemy.explode()
        else:
            self.enemy.timer -= self.enemy.speed/4
        
class Enemy(Sprite):
    def __init__(self, pos, sprite, groups, level_master, player):
        super().__init__(pos, sprite, groups)
        self.tile_pos = (0, 0)
        self.level_master = level_master
        self.player = player
        
        self.behavior = EnemyBehavior(self)

        self.damage = 1
        self.speed = 4
        self.hp = 1

        self.is_alive = True
        self.is_atacking = False

    def move(self, flee=False):
        if flee:
            goal = self.level_master.get_furthest_tile(self.player.tile_pos)
        else:
            goal = self.player.tile_pos

        if self.tile_pos == goal:
            return False
        
        next_step = self.level_master.get_next_step(start=self.tile_pos, goal=goal, max_depth=1e20)
        
        if next_step:
            self.tile_pos = (next_step[0], next_step[1])
            self.rect.center = self.level_master.get_pos_from_tile(self.tile_pos)
            return True
        
        return False
    
    def kill(self):
        super().kill()
        self.is_alive = False

class Chaser(Enemy):
    def __init__(self, pos, sprite, groups, level_master, player):
        super().__init__(pos, sprite, groups, level_master, player)
        self.behavior = ChaserBehavior(self)
        self.speed = 4*2
        self.hp = 3

    def atack(self):
        self.is_atacking = True
        self.player.is_atacked = True
        self.image = self.level_master.game.chaser_atacking_image
        
class Bomber(Enemy):
    def __init__(self, pos, sprite, groups, level_master, player):
        super().__init__(pos, sprite, groups, level_master, player)
        self.bomb_cooldown = 0
        self.behavior = BomberBehavior(self)
        self.speed = 4
    
    def create_bomb(self):
        self.level_master.create_bomb(self.tile_pos)
        self.bomb_cooldown = 4*8

class Bomb(Enemy):
    def __init__(self, pos, sprite, groups, level_master, player):
        super().__init__(pos, sprite, groups, level_master, player)
        self.timer = 4*2
        self.behavior = BombBehavior(self)

    def explode(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                tile_pos = (self.tile_pos[0] + i, self.tile_pos[1] + j)
                if self.level_master.is_tile_movable(tile_pos):
                    Effect(self.level_master.get_pos_from_tile(tile_pos), self.level_master.game.bomb_effect_image, (self.level_master.game.all_sprites, self.level_master.game.effect_sprites))
                if self.level_master.is_occupied_by_player(tile_pos):
                    self.player.hp -= self.damage
        self.kill()

class Effect(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.duration = 4

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()

class Player(Sprite):
    BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w]

    def __init__(self, pos, sprite, groups, level_master):
        super().__init__(pos, sprite, groups)
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
            for enemy in self.level_master.game.enemy_sprites :
                if enemy.is_atacking:
                    atacker = enemy

            atack_dir = tools.coords_sum((-1*self.tile_pos[0], -1*self.tile_pos[1]), atacker.tile_pos)
            if atack_dir == dir:
                atacker.hp -= 1
                if atacker.hp <= 0:
                    atacker.kill()
                    self.is_atacked = False
            else:
                self.hp -= 1
        else:
            new_tile_pos = tools.coords_sum(dir, self.tile_pos)
            enemy = self.level_master.is_occupied_by_enemy(new_tile_pos)
            if enemy:
                pass
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.kill()
            else:
                if self.level_master.is_tile_door(new_tile_pos): self.level_master.change_room(self.level_master.current_room_coords + dir)
                if self.level_master.is_tile_movable(new_tile_pos): self.tile_pos = new_tile_pos

                self.rect.center = self.level_master.get_pos_from_tile(self.tile_pos)

class LevelMaster:
    LEVEL_DIMS = (13, 13)
    TILE_SIZE = 64
    LEVEL_ORIGIN = (TILE_SIZE, TILE_SIZE)
    INDENT = (TILE_SIZE/2, TILE_SIZE/2)
    TILES_ORIGIN = tools.coords_sum(LEVEL_ORIGIN, INDENT)
    
    def __init__(self, game):
        self.game = game

        self.player = Player(self.get_pos_from_tile((2, 2)), self.game.ph_image, (self.game.all_sprites, self.game.player_sprites), self)

        level_generator = LevelGenerator()
        level_generator.generate_level()
        self.level = level_generator.rooms
        self.room_variants = level_generator.room_variants
        self.current_room_coords = (4, 4)
        self.change_room((4, 4))

    def change_room(self, coords):
        tiles = self.room_variants[coords[0]][coords[1]]
        #tiles = [[random.randint(0, 1) for _ in range(self.LEVEL_DIMS[0])] for _ in range(self.LEVEL_DIMS[1])]
        self.LEVEL_DIMS = (len(tiles[0]), len(tiles))
        #self.LEVEL_ORIGIN = ((13-self.LEVEL_DIMS[0])*self.TILE_SIZE, (10-self.LEVEL_DIMS[1])*self.TILE_SIZE)
        
        self.INDENT = (self.TILE_SIZE/2, self.TILE_SIZE/2)
        self.TILES_ORIGIN = tools.coords_sum(self.LEVEL_ORIGIN, self.INDENT)
        self.tiles = []
        self.enemy_spawn_points = []

        for i in range(len(tiles)):
            row = []
            for j in range(len(tiles[0])):
                tile = tiles[i][j]
                match tile:
                    case int():
                        if tile == 1:
                            row.append(Wall((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.wall_image, (self.game.all_sprites, self.game.level_sprites)))
                        elif tile == 0:
                            row.append(Cell((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites)))
                    case str():
                        if tile == 'e_chaser':  
                            self.enemy_spawn_points.append((Chaser, (j, i)))
                            row.append(Cell((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites)))
                        if tile == 'e_bomber':
                            self.enemy_spawn_points.append((Bomber, (j, i)))
                            row.append(Cell((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites)))
                        if tile == 'e_bomb':
                            self.enemy_spawn_points.append((Bomb, (j, i)))
                            row.append(Cell((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites)))
                        if tile.split('_')[-1] == 'door':
                            row.append(Door((tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites), tile.split('_')[0]))
                        
            self.tiles.append(row)
            
        self._create_enemies()

    def _create_enemies(self):
        for enemy_type, spawn_pos in self.enemy_spawn_points:
            pixel_pos = self.get_pos_from_tile(spawn_pos)
            
            if enemy_type == Bomber:
                enemy = Bomber(pixel_pos, self.game.bomber_image, (self.game.all_sprites, self.game.enemy_sprites), self, self.player)
            elif enemy_type == Chaser:
                enemy = Chaser(pixel_pos, self.game.chaser_image, (self.game.all_sprites, self.game.enemy_sprites), self, self.player)
            elif enemy_type == Bomb:
                enemy = Chaser(pixel_pos, self.game.bomb_image, (self.game.all_sprites, self.game.enemy_sprites), self, self.player)
            enemy.tile_pos = spawn_pos

    def get_pos_from_tile(self, tile_pos):
        return tools.coords_sum(self.TILES_ORIGIN, (tile_pos[0] * self.TILE_SIZE, tile_pos[1] * self.TILE_SIZE))
    
    def is_tile_movable(self, tile_pos):
        for i in range(len(self.LEVEL_DIMS)):
            if tile_pos[i] < 0 or tile_pos[i] >= self.LEVEL_DIMS[i]:
                return False
            
        tile = self.tiles[tile_pos[1]][tile_pos[0]]

        if tile.is_movable and not self.is_occupied_by_enemy(tile_pos):
            return True
        
        return False
    
    def is_tile_door(self, tile_pos):
        tile = self.tiles[tile_pos[0]][tile_pos[1]]
        if type(tile) == Door:
            return True
        
        return False
    
    def is_occupied_by_enemy(self, tile_pos):
        for enemy in self.game.enemy_sprites:
            if enemy.tile_pos == tile_pos: 
                return enemy
        return False
    
    def is_occupied_by_player(self, tile_pos):
        return tile_pos == self.player.tile_pos
    
    def create_bomb(self, tile_pos):
        bomb = Bomb(self.get_pos_from_tile(tile_pos), self.game.bomb_image, (self.game.all_sprites, self.game.enemy_sprites), self, self.player)
        bomb.tile_pos = tile_pos
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def a_star_search(self, start, goal, max_depth=1e20):
        closed_set = []
        open_set = [start]
        
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        came_from = {}
        
        while open_set and len(closed_set) < max_depth:
            current = open_set[0]
            for node in open_set:
                if f_score.get(node, float('inf')) < f_score.get(current, float('inf')):
                    current = node
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            open_set.remove(current)
            closed_set.append(current)
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if neighbor in closed_set:
                    continue
                
                if not self.is_tile_movable(neighbor):
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    
                    if neighbor not in open_set:
                        open_set.append(neighbor)
        
        return None
    
    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def get_next_step(self, start, goal, max_depth=1e20):
        path = self.a_star_search(start, goal, max_depth)
        if path and len(path) > 1:
            
            return path[1]
        print(path)
        return None
    
    def get_furthest_tile(self, start_pos):
        queue = [] 
        queue.append((start_pos, 0))
        
        head_index = 0
        
        visited = {start_pos: True}
        
        farthest_pos = start_pos
        max_distance = 0
        
        while head_index < len(queue):
            current_pos, distance = queue[head_index]
            head_index += 1
            
            if distance > max_distance:
                max_distance = distance
                farthest_pos = current_pos
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current_pos[0] + dx, current_pos[1] + dy)
                
                if self.is_tile_movable(neighbor) and neighbor not in visited:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + 1))
        
        return farthest_pos


class MusicMaster:
    def __init__(self, game):
        self.game = game

        self.bpm = 104
        self.beat_duration = 60 / (self.bpm*4)
        self.current_beat = 0
        self.next_beat_time = 0
        self.hit_window = 0.15

        pygame.mixer.music.load(r'music\test1.mp3')
        pygame.mixer.music.set_volume(0.5)

    def is_time_on_beat(self, current_time):
        time_to_beat = (current_time+0.5) % self.beat_duration*4
        return min(time_to_beat, self.beat_duration*4 - time_to_beat) <= self.hit_window
    
    def update_beats(self, current_song_time):
        while current_song_time >= self.next_beat_time:
            self.next_beat_time += self.beat_duration
            self.current_beat += 1
            #print(current_song_time)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((960, 1000))
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.level_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

        self.load_images()
        
        self.level_master = LevelMaster(self)

        self.music_master = MusicMaster(self)

    def load_images(self):
        self.wall_image = pygame.image.load(r"sprites\level\ph-wall.png").convert_alpha()
        self.cell_image = pygame.image.load(r"sprites\level\ph-cell.png").convert_alpha()

        self.ph_image = pygame.image.load(r"sprites\rhythm\ph-1.png").convert_alpha()
        self.ph_image = pygame.transform.scale(self.ph_image, (self.ph_image.get_width() * 2, self.ph_image.get_height() * 2))
    
        self.chaser_image = pygame.image.load(r"sprites\e\e.png").convert_alpha()
        self.chaser_atacking_image = pygame.image.load(r"sprites\e\e_atacking.png").convert_alpha()

        self.bomber_image = pygame.image.load(r"sprites\e\bomber.png").convert_alpha()

        self.bomb_effect_image = pygame.image.load(r"sprites\e\bomb_effect.png").convert_alpha()
        self.bomb_image = pygame.image.load(r"sprites\e\bomb.png").convert_alpha()

    def update_enemies(self):
        for enemy in self.enemy_sprites:
            if self.music_master.current_beat % enemy.speed == 0 and enemy.is_alive:
                enemy.behavior.get_next_action()
            
            if self.level_master.is_occupied_by_player(enemy.tile_pos):
                self.handle_player_defeat()

    def handle_player_defeat(self):
        #print("Игрок пойман! Игра окончена.")
        #pygame.mixer.music.stop()
        #self.running = False
        pass

    def run(self):
        pygame.mixer.music.play()
        dt = 0.1
        last_beat_processed = -1

        while self.running:
            self.screen.fill((255, 255, 255))
            current_song_time = pygame.mixer.music.get_pos() / 1000.0
            self.music_master.update_beats(current_song_time)

            if self.music_master.current_beat > last_beat_processed:
                self.effect_sprites.update()
                self.update_enemies()
                last_beat_processed = self.music_master.current_beat

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.level_master.player.BINDS and self.music_master.is_time_on_beat(current_song_time):
                        self.level_master.player.handle_input(event.key)
                        
                        for enemy in self.enemy_sprites:
                            if self.level_master.is_occupied_by_player(enemy.tile_pos):
                                self.handle_player_defeat()

            self.level_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.effect_sprites.draw(self.screen)
            #self.all_sprites.draw(self.screen)
            
            pygame.display.flip()
            
            dt = self.clock.tick(240) / 1000
            dt = max(0.001, min(0.1, dt))

if __name__ == '__main__':
    game = Game()
    game.run()
