import pygame
from ui.ui_component import UIComponent
from settings import *

class MiniMap(UIComponent):
    def __init__(self, origin_pos, assets, level_master):
        super().__init__(origin_pos, assets)
        self.level_master = level_master
        
        self.cell_size = 16 
        self.padding = 2 
        
        self.color_room_visited = (100, 100, 100)   
        self.color_room_current = (255, 255, 255) 
        self.color_door = (200, 200, 200)        
        self.color_background = (30, 30, 30)       
        
    def draw(self, screen):
        map_width = 9 * (self.cell_size + self.padding)
        map_height = 9 * (self.cell_size + self.padding)
        map_surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        
        map_surface.fill(self.color_background)
        
        rooms = self.level_master.generator.rooms
        room_variants = self.level_master.generator.room_variants
        visited_rooms = self.level_master.visited_rooms
        current_room = self.level_master.current_room_coords
        
        for y in range(9):
            for x in range(9):
                if (x, y) in visited_rooms:
                    px = x * (self.cell_size + self.padding)
                    py = y * (self.cell_size + self.padding)
                    
                    if (x, y) == current_room:
                        color = self.color_room_current
                    else:
                        color = self.color_room_visited
                    
                    pygame.draw.rect(map_surface, color, 
                                   (px, py, self.cell_size, self.cell_size))
                    
                    room_data = room_variants[y][x]
                    self._draw_doors(map_surface, room_data, px, py)

        screen.blit(map_surface, self.origin_pos)
    
    def _draw_doors(self, surface, room_data, px, py):
        door_size = 4 
        half_cell = self.cell_size // 2
        
        for row in room_data:
            for cell in row:
                if cell == 'top_door':
                    dx = px + half_cell - door_size // 2
                    dy = py - door_size // 2
                    pygame.draw.rect(surface, self.color_door, (dx, dy, door_size, door_size))
                elif cell == 'bottom_door':
                    dx = px + half_cell - door_size // 2
                    dy = py + self.cell_size - door_size // 2
                    pygame.draw.rect(surface, self.color_door, (dx, dy, door_size, door_size))
                elif cell == 'left_door':
                    dx = px - door_size // 2
                    dy = py + half_cell - door_size // 2
                    pygame.draw.rect(surface, self.color_door, (dx, dy, door_size, door_size))
                elif cell == 'right_door':
                    dx = px + self.cell_size - door_size // 2
                    dy = py + half_cell - door_size // 2
                    pygame.draw.rect(surface, self.color_door, (dx, dy, door_size, door_size))