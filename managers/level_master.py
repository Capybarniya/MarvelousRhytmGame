from random import choice
from sprites import Wall, Cell, Door, Shrine
from sprites import Chaser, Bomber, Bomb, Player
from sprites import Effect, EffectSpawner
from utils import a_star_search, get_furthest_tile, LevelGenerator
from utils import tools
from settings import *

class LevelMaster:
    TILE_SIZE = 64
    LEVEL_ORIGIN = (TILE_SIZE, TILE_SIZE)
    
    def __init__(self, game_mode, assets):
        self.game = game_mode
        self.assets = assets
        self.player = Player((-100, -100), self.assets, (self.game.player_sprites), self)
        self.effect_spawner = EffectSpawner(self.assets, self.game.effect_sprites)
        
        self.generator = None
        self.visited_rooms = set()

    def generate_level(self):
        self.generator = LevelGenerator()
        self.generator.generate_level()
        self.level = self.generator.rooms
        self.room_variants = self.generator.room_variants

    def start(self):
        self.current_room_coords = (4, 4)
        self.visited_rooms.add(self.current_room_coords)
        self.change_room((4, 4))
        self.player.move_to_the_start_pos()
    
    def change_room(self, coords):
        x, y = coords[0], coords[1]
        
        self.visited_rooms.add(coords)
        
        self._kill_room()
        self.current_room_coords = coords
        
        room_data = self.room_variants[y][x]

        tiles = room_data
        room_width_tiles = len(tiles[0])
        room_height_tiles = len(tiles)
        self.LEVEL_DIMS = (room_width_tiles, room_height_tiles)
        
        room_width_px = room_width_tiles * self.TILE_SIZE
        room_height_px = room_height_tiles * self.TILE_SIZE
        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT
        
        offset_x = (screen_width - room_width_px) / 2
        offset_y = (screen_height - room_height_px) / 2
        
        self.INDENT = (self.TILE_SIZE / 2, self.TILE_SIZE / 2+64)
        self.TILES_ORIGIN = (offset_x + self.INDENT[0], offset_y + self.INDENT[1])

        for i in range(len(tiles)):
            row = []
            for j in range(len(tiles[0])):
                tile = tiles[i][j]
                tile_pos = (tools.coords_sum(self.TILES_ORIGIN, (self.TILE_SIZE*j, self.TILE_SIZE*i)))
                level_groups = (self.game.level_sprites)
                match tile:
                    case int():
                        if tile == 1:
                            row.append(Wall(tile_pos, self.assets, level_groups))
                        elif tile == 0:
                            row.append(Cell(tile_pos, self.assets, level_groups))
                    case str():
                        if tile == 'e_chaser':  
                            self.enemy_spawn_points.append((Chaser, (j, i)))
                            row.append(Cell(tile_pos, self.assets, level_groups))
                        elif tile == 'e_bomber':
                            self.enemy_spawn_points.append((Bomber, (j, i)))
                            row.append(Cell(tile_pos, self.assets, level_groups))
                        elif tile == 'e_bomb':
                            self.enemy_spawn_points.append((Bomb, (j, i)))
                            row.append(Cell(tile_pos, self.assets, level_groups))
                        elif tile.split('_')[-1] == 'door':
                            row.append(Door(tile_pos, self.assets, level_groups, tile.split('_')[0]))
                        elif tile == 'shrine':
                            row.append(Shrine(tile_pos, self.assets, level_groups))
                        else:
                            print(f"ошибка парсинга, замена ячейкой")
                            row.append(Cell(tile_pos, self.assets, level_groups))
            self.tiles.append(row)
            
        self._create_enemies()

    def _kill_room(self):
        self.game.level_sprites.empty()
        self.game.enemy_sprites.empty()
        self.game.effect_sprites.empty()
        self.tiles = []
        self.enemy_spawn_points = []

    def _create_enemies(self):
        for enemy_type, spawn_pos in self.enemy_spawn_points:
            pixel_pos = self.get_pos_from_tile(spawn_pos)
            enemy_groups = (self.game.enemy_sprites)
            
            if enemy_type == Bomber:
                enemy = Bomber(pixel_pos, self.assets, enemy_groups, self, self.player)
            elif enemy_type == Chaser:
                enemy = Chaser(pixel_pos, self.assets, enemy_groups, self, self.player)
            elif enemy_type == Bomb:
                enemy = Bomb(pixel_pos, self.assets, enemy_groups, self, self.player, self.effect_spawner)
            enemy.tile_pos = spawn_pos

    def get_pos_from_tile(self, tile_pos):
        return tools.coords_sum(self.TILES_ORIGIN, (tile_pos[0] * self.TILE_SIZE, tile_pos[1] * self.TILE_SIZE))
    
    def get_door(self, tile_pos):
        tile = self.tiles[tile_pos[1]][tile_pos[0]]
        if type(tile) == Door:
            return tile
        
        return False

    def get_pair_pos_from_door(self, door):
        pairs = {
            'right': 'left',
            'left': 'right',
            'top': 'down',
            'down': 'top',
        }
        new_door_dir = pairs[door.direction]
        for i in range(len(self.tiles)):     
            for j in range(len(self.tiles[i])): 
                tile = self.tiles[i][j]        
                if type(tile) == Door and new_door_dir == tile.direction:
                    return (j, i)
        return (2, 2)
    
    def get_random_tile(self, tile_pos, check_for_movable=True):
        x, y = tile_pos
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        candidates = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < self.LEVEL_DIMS[0] and 0 <= ny < self.LEVEL_DIMS[1]:
                if check_for_movable:
                    if self.is_tile_movable((nx, ny), check_for_enemies=True):
                        candidates.append((nx, ny))
                else:
                    candidates.append((nx, ny))

        return choice(candidates) if candidates else tile_pos
    
    def is_tile_movable(self, tile_pos, check_for_enemies=True):
        for i in range(len(self.LEVEL_DIMS)):
            if tile_pos[i] < 0 or tile_pos[i] >= self.LEVEL_DIMS[i]:
                return False
            
        tile = self.tiles[tile_pos[1]][tile_pos[0]]

        if check_for_enemies:
            if tile.is_movable and not self.is_occupied_by_enemy(tile_pos):
                return True
        else:
            if tile.is_movable:
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
        bomb = Bomb(self.get_pos_from_tile(tile_pos), self.assets, (self.game.enemy_sprites), self, self.player, self.effect_spawner)
        bomb.tile_pos = tile_pos

    def cleanup(self): pass

    def check_for_shrine(self, tile_pos):
        tile = self.tiles[tile_pos[1]][tile_pos[0]]
        if type(tile) == Shrine:
            exit_event = pygame.event.Event(SHRINE_FOUND_EVENT)
            pygame.event.post(exit_event)
