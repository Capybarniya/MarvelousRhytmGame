import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite 
        self.rect = self.image.get_frect(center = pos)

class Projectile(Sprite):
    def __init__(self, master, origin, sprite, groups):
        super().__init__(master.ORIGINS[origin], sprite, groups)
        self.origin = origin
        self.hitbox_rect = self.rect.inflate(-8, -8)
        
    def move(self, y, dt):
        self.hitbox_rect.y += y * dt
        self.rect.center = self.hitbox_rect.center

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

class BeatLine(Sprite):
    def __init__(self, master, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class ProjectileMaster:
    ORIGINS = [(200, 0), (300, 0), (400, 0), (500, 0), (600, 0)]
    ORIGINS_BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

    def __init__(self, game):
        self.game = game
        self.x = 200
        self.y = 0
        self.projectiles = pygame.sprite.Group()
        self.last_beat_time = 0
        self.hitbox_image = pygame.image.load(r"sprites\ph-master-hb.png").convert_alpha()
        #self.hitbox_image = pygame.transform.scale(self.hitbox_image, (self.hitbox_image.get_width() * 2, self.hitbox_image.get_height() * 2))
        self.beat_line = BeatLine(self, (400, 900), self.hitbox_image, self.game.all_sprites)
        self.playlist = game.playlist1
        self.bpm = 140
        self.cur_beat = 0

    def init_song(self):
        pass

    def beat(self):
        for i in range(len(self.playlist[self.cur_beat][1])):
            if self.playlist[self.cur_beat][1][i]:
                self.spawn_projectile(i)
        self.cur_beat += 1

    def spawn_projectile(self, origin):
        projectile = Projectile(self, origin, self.game.ph_image, (self.projectiles, self.game.all_sprites))

class Game:
    BEAT_EVENT = pygame.event.custom_type()
    playlist1 = [
        (4, [1, 0, 0, 0, 0]),
        (4, [0, 1, 0, 0, 0]),
        (4, [0, 0, 0, 0, 1]),
        (4, [1, 0, 1, 0, 1]),
        (2, [1, 0, 0, 0, 0]),
        (6, [1, 0, 0, 0, 0]),
        (4, [1, 0, 0, 0, 1]),
        (4, [1, 0, 1, 0, 1]),
        (1, [1, 0, 0, 0, 0]),
        (1, [1, 0, 0, 0, 0]),
        (1, [1, 1, 0, 0, 0]),
        (1, [1, 1, 0, 0, 0]),
        (1, [1, 1, 1, 0, 0]),
        (1, [1, 1, 1, 0, 0]),
        (1, [1, 1, 1, 1, 0]),
        (1, [1, 1, 1, 1, 0]),

    ]
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((800, 1000))
        self.all_sprites = pygame.sprite.Group()
        self.master = ProjectileMaster(self)

        self.load_images()

    def load_images(self):
        self.ph_image = pygame.image.load(r"sprites\ph-1.png").convert_alpha()
        self.ph_image = pygame.transform.scale(self.ph_image, (self.ph_image.get_width() * 2, self.ph_image.get_height() * 2))

    def run(self):
        d_time = 0.1
        total_time = 0

        while self.running:
            self.screen.fill((255, 255, 255))

            for sprite in self.master.projectiles.sprites():
                if self.master.beat_line.rect.colliderect(sprite.hitbox_rect): 
                    #print(sprite.hitbox_rect.center)
                    beat_event = pygame.event.Event(self.BEAT_EVENT, {'sprite': sprite})  
                    pygame.event.post(beat_event)
            
            beat_len = 60 / (self.master.bpm*4)
            if self.master.cur_beat >= len(self.master.playlist):
                self.master.cur_beat = 0
            if total_time - (beat_len*self.playlist1[self.master.cur_beat][0]) >= self.master.last_beat_time: 
                self.master.beat()
                self.master.last_beat_time = total_time

            for sprite in self.master.projectiles.sprites(): sprite.move(self.master.bpm*4, d_time)

            self.all_sprites.draw(self.screen)

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.BEAT_EVENT:
                    for i in range(len(self.master.ORIGINS)):
                        if event.sprite.origin == i and keys[self.master.ORIGINS_BINDS[i]]:
                            event.sprite.kill()



            pygame.display.flip()

            d_time = self.clock.tick(120) / 1000
            d_time = max(0.001, min(0.1, d_time))
            total_time += d_time

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 
