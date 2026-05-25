import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite
        self.rect = self.image.get_frect(center=pos)

class Projectile(Sprite):
    def __init__(self, master, origin, sprite, groups, origin_time):
        super().__init__(master.ORIGINS[origin], sprite, groups)
        self.origin = origin
        self.master = master
        self.origin_time = origin_time
        self.hitbox_rect = self.rect.inflate(80, 80)
        self.triggered = False

    def move(self):
        BPM = self.master.bpm
        TRACK_LENGTH = 2
        BEAT_DURATION = 60 / BPM
        TRACK_DURATION = BEAT_DURATION * TRACK_LENGTH
        TRACK_HEIGHT = 900

        current_time = pygame.mixer.music.get_pos() / 1000.0
        time_since_origin = current_time - self.origin_time
        progress = time_since_origin / TRACK_DURATION

        start_y = -50
        end_y = TRACK_HEIGHT - self.hitbox_rect.height
        self.hitbox_rect.y = start_y + progress * (end_y - start_y)
        self.rect.center = self.hitbox_rect.center

class BeatLine(Sprite):
    def __init__(self, master, pos, sprite, groups):
        super().__init__(pos, sprite, groups)

class ProjectileMaster:
    ORIGINS = [(200, -50), (300, -50), (400, -50), (500, -50), (600, -50)]
    ORIGINS_BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

    def __init__(self, game):
        self.game = game
        self.projectiles = pygame.sprite.Group()
        self.bpm = 104
        self.beat_duration = 60 / self.bpm
        self.cur_beat = 0
        self.next_beat_time = 0.0
        self.score = 0
        self.playlist = game.playlist1
        self.key_cooldowns = {k: 0.0 for k in self.ORIGINS_BINDS}
        self.input_cooldown = 0.25
        self.hit_window = 100

        self.hitbox_image = pygame.image.load(r"sprites\ph-master-hb.png").convert_alpha()
        self.score_line = BeatLine(self, (400, 900), self.hitbox_image, self.game.all_sprites)
        self.miss_line = pygame.Rect(200, 950, 400, 100)

        pygame.mixer.music.load(r'music\test1.mp3')
        pygame.mixer.music.set_volume(0.5)

    def update_beats(self, current_song_time):
        while self.cur_beat < len(self.playlist) and current_song_time >= self.next_beat_time:
            self._spawn_current_beat()
            beat_count, _ = self.playlist[self.cur_beat]
            self.next_beat_time += beat_count * self.beat_duration/4
            self.cur_beat += 1

    def _spawn_current_beat(self):
        if self.cur_beat >= len(self.playlist):
            return
        _, lanes = self.playlist[self.cur_beat]
        current_time = pygame.mixer.music.get_pos() / 1000.0
        for i, active in enumerate(lanes):
            if active:
                self.spawn_projectile(i, current_time)

    def spawn_projectile(self, origin, current_time):
        Projectile(self, origin, self.game.ph_image, (self.projectiles, self.game.all_sprites), current_time)

    def handle_input(self, key, current_time):
        if current_time < self.key_cooldowns[key]:
            return

        origin_idx = self.ORIGINS_BINDS.index(key)
        target_y = self.score_line.rect.centery
        closest_proj = None
        min_dist = float('inf')

        for proj in self.projectiles.sprites():
            if proj.origin == origin_idx and not proj.triggered:
                dist = abs(proj.hitbox_rect.centery - target_y)
                if dist < min_dist and dist <= self.hit_window:
                    min_dist = dist
                    closest_proj = proj

        if closest_proj:
            closest_proj.triggered = True
            closest_proj.kill()
            self.score += 20
            self.key_cooldowns[key] = current_time + self.input_cooldown

    def check_misses(self):
        for proj in self.projectiles.sprites():
            if not proj.triggered and proj.hitbox_rect.bottom > self.miss_line.top:
                proj.triggered = True
                proj.kill()
                self.score = 0

class Game:
    begining = [
        (4,[0, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),
        (1,[1, 0, 0, 0, 0]),]
    
    seg_A = [
        (2, [1, 0, 0, 0, 0]), (1, [0, 1, 0, 0, 0]), (3, [0, 0, 1, 0, 0]),
        (1, [0, 1, 0, 0, 0]), (1, [0, 0, 1, 0, 0]), (2, [1, 0, 0, 0, 0]),
        (2, [0, 1, 0, 0, 0]), (2, [0, 0, 0, 0, 1]), (2, [0, 0, 0, 1, 0]),]
    
    seg_B = [
        (8, [1, 0, 1, 0, 1]), (4, [0, 1, 0, 1, 0]), (2, [0, 0, 0, 1, 0]), (2, [0, 0, 0, 0, 1]),]
    
    seg_C = [
        (8, [1, 0, 1, 0, 1]), (3, [0, 1, 0, 1, 0]), (3, [0, 0, 0, 1, 0]), (2, [0, 1, 0, 0, 0]),]
    
    seg_D = [(6, [1, 0, 1, 0, 1]), (10, [0, 1, 0, 1, 0]), (6, [1, 0, 1, 0, 1]), (10, [0, 1, 0, 1, 0])]
    seg_E = [(6, [1, 0, 1, 0, 1]), (2, [0, 1, 0, 1, 0]), (4, [0, 1, 0, 1, 0]), (4, [0, 1, 0, 1, 0]),
             (4, [1, 1, 0, 0, 0]), (4, [0, 1, 1, 0, 0]), (4, [0, 0, 0, 1, 1]), (4, [0, 0, 1, 1, 0])]
    seg_F = [(6, [1, 0, 1, 0, 1]), (10, [0, 1, 0, 1, 0]), (8, [0, 1, 0, 1, 0]), (8, [0, 1, 0, 1, 0])]
    
    seg_T = seg_D + seg_E + seg_D + seg_F
    playlist1 = begining + seg_A + seg_B + seg_A + seg_B + seg_A + seg_B + seg_A + seg_C + seg_T + seg_T

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
        pygame.mixer.music.play()
        dt = 0.1
        total_time = 0

        while self.running:
            self.screen.fill((255, 255, 255))
            current_song_time = pygame.mixer.music.get_pos() / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.master.ORIGINS_BINDS:
                        self.master.handle_input(event.key, current_song_time)

            self.master.update_beats(current_song_time)

            for proj in self.master.projectiles.sprites():
                proj.move()

            self.master.check_misses()

            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000
            dt = max(0.001, min(0.1, dt))
            total_time += dt

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
