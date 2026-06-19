from utils import heuristic

class EnemyBehavior:
    def __init__(self, enemy):
        self.enemy = enemy

    def get_next_action(self):
        pass

class ChaserBehavior(EnemyBehavior):
    def __init__(self, enemy):
        super().__init__(enemy)

    def get_next_action(self):
        if heuristic(self.enemy.tile_pos, self.enemy.player.tile_pos) <= 1:
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
            if heuristic(self.enemy.tile_pos, self.enemy.player.tile_pos) < 3:
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