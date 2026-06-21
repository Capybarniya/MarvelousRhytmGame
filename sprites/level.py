from sprites.sprite import Sprite

from settings import * 

class Tile(Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(pos, sprite, groups)
        self.is_movable = True

class Wall(Tile):
    def __init__(self, pos, assets, groups):
        sprite = assets.get_image(WALL_IMAGE)
        super().__init__(pos, sprite, groups)
        self.is_movable = False

class Cell(Tile):
    def __init__(self, pos, assets, groups):
        sprite = assets.get_image(CELL_IMAGE)
        super().__init__(pos, sprite, groups)

class Door(Tile):
    def __init__(self, pos, assets, groups, direction):
        sprite = assets.get_image(CELL_IMAGE)
        super().__init__(pos, sprite, groups)
        self.direction = direction

class Shrine(Tile):
    def __init__(self, pos, assets, groups):
        sprite = assets.get_image(SHRINE_IMAGE)
        super().__init__(pos, sprite, groups)