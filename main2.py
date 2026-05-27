import random

import pygame

import tools

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite
        self.rect = self.image.get_frect(center=pos)

class Wall(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class Cell(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class Player(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class LevelMaster:
    LEVEL_DIMS = (15, 15)
    LEVEL_ORIGIN = (0, 0)
    TILE_SIZE = 64
    
    def __init__(self, game):
        self.game = game

    def create_level(self):
        #tiles = [[random.randint(0, 1) for _ in range(self.LEVEL_DIMS[0])] for _ in range(self.LEVEL_DIMS[1])]
        tiles = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.tiles = []
        indent = (self.TILE_SIZE/2, self.TILE_SIZE/2)
        for i in range(self.LEVEL_DIMS[1]):
            row = []
            for j in range(self.LEVEL_DIMS[0]):
                if tiles[i][j] == 1:
                    row.append(Wall((tools.coords_sum(indent, self.LEVEL_ORIGIN, (64*j, 64*i))), self.game.wall_image, (self.game.all_sprites, self.game.level_sprites)))
                elif tiles[i][j] == 0:
                    row.append(Cell((tools.coords_sum(indent, self.LEVEL_ORIGIN, (64*j, 64*i))), self.game.cell_image, (self.game.all_sprites, self.game.level_sprites)))

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((960, 1000))
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.level_sprites = pygame.sprite.Group()

        self.load_images()
        
        self.level_master = LevelMaster(self)
        self.level_master.create_level()

        self.player = Player((32, 32), self.ph_image, (self.all_sprites, self.player_sprites))

    def load_images(self):
        self.wall_image = pygame.image.load(r"sprites\level\ph-wall.png").convert_alpha()
        self.cell_image = pygame.image.load(r"sprites\level\ph-cell.png").convert_alpha()
        self.ph_image = pygame.image.load(r"sprites\rhythm\ph-1.png").convert_alpha()
        self.ph_image = pygame.transform.scale(self.ph_image, (self.ph_image.get_width() * 2, self.ph_image.get_height() * 2))

    def run(self):
        dt = 0.1

        while self.running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.level_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            
            dt = self.clock.tick(60) / 1000
            dt = max(0.001, min(0.1, dt))

if __name__ == '__main__':
    game = Game()
    game.run()
