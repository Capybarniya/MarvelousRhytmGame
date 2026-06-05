from random import random, randint

room1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0,],
         [0, 0, 1, 0, 1, 0, 1, 0, 0,],
         [0, 0, 'e_bomba', 0, 0, 'e_chaser', 0, 0, 0,]]

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


class LevelGenerator:
    VARIANTS = [room1, room2, room3, room4]
    def __init__(self):
        self.rooms = [[0 for _ in range(9)] for _ in range(9)]
        self.room_variants = [[0 for _ in range(9)] for _ in range(9)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def generate_level(self):
        self.rooms[4][4] = 1
        for _ in range(10):
            for i in range(1,8):
                for j in range(1,8):
                    start_room_dist = self.heuristic((i, j), (7, 7))
                    rooms_nearby = 0
                    for k in (range(-1, 2)):
                        for l in range(-1, 2):
                            if not abs(k) == abs(l):
                                if self.rooms[i+k][j+l] == 1:
                                    rooms_nearby += 1
                    if rooms_nearby:
                        r = random()
                        chance = 0.1*(10-start_room_dist - rooms_nearby*4)+0.1
                        if r <= chance: 
                            self.rooms[i][j] = 1
        #self.print_matrix(self.rooms)
        self._generate_room_variants()


    def _generate_room_variants(self):
        for i in range(1,8):
            for j in range(1,8):
                if self.rooms[i][j]:
                    var = self.VARIANTS[randint(0, len(self.VARIANTS)-1)]
                    var = self.create_borders(var, (i, j))
                    self.room_variants[i][j] = var

    def print_matrix(self, matrix):
        for row in matrix:
            print(' '.join(f'{x:3}' for x in row))

    def create_borders(self, room, coords):
        new_room = []
        for row in room:
            new_row = [1] + row + [1]
            new_room += [new_row]
        new_room = [[1]*len(new_room [0])] + new_room  + [[1]*len(new_room [0])]
        #print(room)

        nearby_rooms = self.get_nearby_rooms(coords)
        top_coords = (0, int(len(new_room[0])/2))
        right_coords = (int(len(new_room)/2), len(new_room[0])-1)
        down_coords = (len(new_room)-1, int(len(new_room[0])/2))
        left_coords = (int(len(new_room)/2) , 0)
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
        nearby_rooms = [[0 for _ in range(3)] for _ in range(3)]
        leap = [1, 2, 0]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not abs(i) == abs(j):
                    if self.rooms[coords[0]+i][coords[1]+j] == 1:
                        k, l = leap[i], leap[j]
                        nearby_rooms[k][l] = 1
        return nearby_rooms
                        
'''l_g = LevelGenerator()
l_g.generate_level()
test_room = [[0 for _ in range(9)] for _ in range(9)]
test_room = room1
test_room = l_g.create_borders(test_room, (4, 4))
l_g.print_matrix(test_room)'''


