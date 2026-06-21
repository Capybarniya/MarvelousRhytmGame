from random import random, randint

room1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 1, 0, 1, 0, 1, 0, 0,],
         [0, 0, 'e_bomb', 0, 0, 'e_chaser', 0, 0, 0,]]

room2 = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 'e_bomber', 0, 0],
         [0, 1, 1, 1, 1, 1, 0],
         [0, 0, 'e_bomber', 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]]

room3 = [[1, 0, 1],
         [0, 0, 0],
         [0, 0, 0],
         [0, 1, 0],
         [0, 'e_chaser', 0],
         [0, 0, 0],
         [1, 0, 1]]

room4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 1, 0, 0, 1, 0, 0, 1, 0,],
         [0, 0, 0, 0, 1, 0, 0, 'e_bomber', 0,],
         [0, 0, 0, 'e_chaser', 1, 'e_chaser', 0, 0, 0,],
         [0, 0, 0, 0, 1, 0, 0, 'e_bomber', 0,],
         [0, 1, 0, 0, 1, 0, 0, 1, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0, 0,],]

final_room = [[0, 0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 1, 0, 0, 1, 0, 0, 1, 0,],
         [0, 0, 0, 0, 'shrine', 0, 0, 0, 0,],
         [0, 0, 0, 'shrine', 1, 'shrine', 0, 0, 0,],
         [0, 0, 0, 0, 'shrine', 0, 0, 0, 0,],
         [0, 1, 0, 0, 1, 0, 0, 1, 0,],
         [0, 0, 0, 0, 0, 0, 0, 0, 0,],]


class LevelGenerator:
    VARIANTS = [room1, room2, room3, room4]
    
    def __init__(self):
        self.rooms = [[0 for _ in range(9)] for _ in range(9)]
        self.room_variants = [[0 for _ in range(9)] for _ in range(9)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def generate_level(self):
        self.rooms[4][4] = 1
        for _ in range(15):
            for y in range(1, 8):
                for x in range(1, 8):
                    start_room_dist = self.heuristic((x, y), (4, 4))
                    
                    rooms_nearby = 0
                    if y - 1 >= 0 and self.rooms[y - 1][x] == 1: rooms_nearby += 1 
                    if y + 1 < 9 and self.rooms[y + 1][x] == 1: rooms_nearby += 1 
                    if x - 1 >= 0 and self.rooms[y][x - 1] == 1: rooms_nearby += 1 
                    if x + 1 < 9 and self.rooms[y][x + 1] == 1: rooms_nearby += 1 
                    
                    if rooms_nearby > 0:
                        r = random()
                        raw_chance = 0.1 * (10 - start_room_dist - rooms_nearby * 4) + 0.1
                        chance = max(0.05, min(1.0, raw_chance))
                        
                        if r <= chance: 
                            self.rooms[y][x] = 1
        
        self._generate_room_variants()

    def _generate_room_variants(self):
        for y in range(1, 8):
            for x in range(1, 8):
                if (x, y) == (4, 4):
                    var = final_room
                    var = self.create_borders(var, (x, y))
                    self.room_variants[y][x] = var
                    print(var)
                elif self.rooms[y][x]:
                    var = self.VARIANTS[randint(0, len(self.VARIANTS)-1)]
                    var = self.create_borders(var, (x, y))
                    self.room_variants[y][x] = var

    def create_borders(self, room, coords):
        x, y = coords[0], coords[1]
        new_room = []
        for row in room:
            new_row = [1] + row + [1]
            new_room.append(new_row)
        new_room = [[1]*len(new_room[0])] + new_room + [[1]*len(new_room[0])]

        nearby_rooms = self.get_nearby_rooms((x, y))
        
        top_coords = (0, len(new_room[0]) // 2)
        right_coords = (len(new_room) // 2, len(new_room[0]) - 1)
        down_coords = (len(new_room) - 1, len(new_room[0]) // 2)
        left_coords = (len(new_room) // 2, 0)
        
        if nearby_rooms[0][1]:
            new_room[top_coords[0]][top_coords[1]] = 'top_door'
        if nearby_rooms[1][2]:
            new_room[right_coords[0]][right_coords[1]] = 'right_door'
        if nearby_rooms[2][1]:
            new_room[down_coords[0]][down_coords[1]] = 'down_door'
        if nearby_rooms[1][0]:
            new_room[left_coords[0]][left_coords[1]] = 'left_door'
            
        return new_room
    
    def get_nearby_rooms(self, coords):
        x, y = coords[0], coords[1]
        nearby_rooms = [[0 for _ in range(3)] for _ in range(3)]
        
        if y - 1 >= 0 and self.rooms[y - 1][x] == 1:
            nearby_rooms[0][1] = 1
        if x + 1 < 9 and self.rooms[y][x + 1] == 1:
            nearby_rooms[1][2] = 1 
        if y + 1 < 9 and self.rooms[y + 1][x] == 1:
            nearby_rooms[2][1] = 1 
        if x - 1 >= 0 and self.rooms[y][x - 1] == 1:
            nearby_rooms[1][0] = 1
            
        return nearby_rooms
                        
#l_g = LevelGenerator()
#l_g.generate_level()
#print(*l_g.room_variants, sep='\n')
#l_g.print_matrix(l_g.room_variants)


