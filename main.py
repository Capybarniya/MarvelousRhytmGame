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
        self.master = master
        self.hitbox_rect = self.rect.inflate(80, 80)
        
    def move(self, dt):
        v = (900*self.master.bpm*4) / (60*8)
        self.hitbox_rect.y += v * dt
        self.rect.center = self.hitbox_rect.center

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

class BeatLine(Sprite):
    def __init__(self, master, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class ProjectileMaster:
    ORIGINS = [(200, -50), (300, -50), (400, -50), (500, -50), (600, -50)]
    ORIGINS_BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

    def __init__(self, game):
        self.game = game

        self.x = 200
        self.y = 0

        self.projectiles = pygame.sprite.Group()

        self.last_beat_time = 0
        self.hitbox_image = pygame.image.load(r"sprites\ph-master-hb.png").convert_alpha()
        self.score_line = BeatLine(self, (400, 900), self.hitbox_image, self.game.all_sprites)
        self.miss_line = pygame.Rect(200, 950, 400, 100)

        self.playlist = game.playlist1
        self.bpm = 104
        self.cur_beat = 1
        self.score = 0

        pygame.mixer.music.load(r'music\test1.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

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
    MISS_EVENT = pygame.event.custom_type()

    begining = [
        (4,[0, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),]
    
    seg_A = [
        (2, [1, 0, 0, 0, 0]),
        (1, [0, 1, 0, 0, 0]),
        (3, [0, 0, 1, 0, 0]),
        (1, [0, 1, 0, 0, 0]),
        (1, [0, 0, 1, 0, 0]),
        
        (2, [1, 0, 0, 0, 0]),
        (2, [0, 1, 0, 0, 0]),
        (2, [0, 0, 0, 0, 1]),
        (2, [0, 0, 0, 1, 0]),]
    
    seg_B = [
        (8, [1, 0, 1, 0, 1]),
        (4, [0, 1, 0, 1, 0]),
        (2, [0, 0, 0, 1, 0]),
        (2, [0, 0, 0, 0, 1]),
        ]
    
    seg_C = [
        (8, [1, 0, 1, 0, 1]),
        (3, [0, 1, 0, 1, 0]),
        (3, [0, 0, 0, 1, 0]),
        (2, [0, 1, 0, 0, 0]),
        ]

    seg_D = [
        (6, [1, 0, 1, 0, 1]),
        (10, [0, 1, 0, 1, 0]),
        (6, [1, 0, 1, 0, 1]),
        (10, [0, 1, 0, 1, 0]),
        ]
    
    seg_E = [
        (6, [1, 0, 1, 0, 1]),
        (2, [0, 1, 0, 1, 0]),
        (4, [0, 1, 0, 1, 0]),
        (4, [0, 1, 0, 1, 0]),
        (4, [1, 1, 0, 0, 0]),
        (4, [0, 1, 1, 0, 0]),
        (4, [0, 0, 0, 1, 1]),
        (4, [0, 0, 1, 1, 0]),
        ]
    
    seg_F = [
        (6, [1, 0, 1, 0, 1]),
        (10, [0, 1, 0, 1, 0]),
        (8, [0, 1, 0, 1, 0]),
        (8, [0, 1, 0, 1, 0]),
    ]

    seg_T = seg_D+seg_E+seg_D+seg_F

    playlist1 = begining+seg_A+seg_B+seg_A+seg_B+seg_A+seg_B+seg_A+seg_C+seg_T+seg_T
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 1000))

        self.running = True
    
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
                if self.master.score_line.rect.colliderect(sprite.hitbox_rect): 
                    beat_event = pygame.event.Event(self.BEAT_EVENT, {'sprite': sprite})  
                    pygame.event.post(beat_event)
                if self.master.miss_line.colliderect(sprite.hitbox_rect): 
                    miss_event = pygame.event.Event(self.MISS_EVENT, {'sprite': sprite})  
                    pygame.event.post(miss_event)
            
            beat_len = 60 / (self.master.bpm*4)
            if self.master.cur_beat >= len(self.master.playlist):
                self.master.cur_beat = 1
            if pygame.mixer.music.get_pos()/1000 - (beat_len*self.playlist1[self.master.cur_beat-1][0]) >= self.master.last_beat_time:
                #print(self.master.last_beat_time, pygame.mixer.music.get_pos()/1000, beat_len, pygame.mixer.music.get_pos()/1000-self.master.last_beat_time)
                self.master.beat()
                self.master.last_beat_time = pygame.mixer.music.get_pos()/1000
                

            for sprite in self.master.projectiles.sprites(): sprite.move(d_time)

            self.all_sprites.draw(self.screen)
            #pygame.draw.rect(self.screen, 'red', (200, 950, 400, 100))

            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.BEAT_EVENT:
                    for i in range(len(self.master.ORIGINS)):
                        if event.sprite.origin == i and keys[self.master.ORIGINS_BINDS[i]]:
                            event.sprite.kill()
                            self.master.score += 20
                            #print(self.master.score)
                if event.type == self.MISS_EVENT:
                    event.sprite.kill()
                    self.master.score = 0
                    ##print(self.master.score)

            pygame.display.flip()

            d_time = self.clock.tick(1000) / 1000
            d_time = max(0.001, min(0.1, d_time))
            total_time += d_time

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 
