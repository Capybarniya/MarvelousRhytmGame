import pygame

from playlists import playlist_test

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, groups):
        super().__init__(groups)
        self.image = sprite
        self.rect = self.image.get_frect(center=pos)

class TapNote(Sprite):
    def __init__(self, master, origin, sprite, groups, origin_time):
        super().__init__(master.ORIGINS[origin], sprite, groups)
        self.origin = origin
        self.master = master
        self.origin_time = origin_time
        self.hitbox_rect = self.rect.inflate(80, 80)

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

class NoteMaster:
    ORIGINS = [(200, -50), (300, -50), (400, -50), (500, -50), (600, -50)]
    ORIGINS_BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

    def __init__(self, game):
        self.game = game
        self.notes = pygame.sprite.Group()

        self.bpm = 104
        self.beat_duration = 60 / (self.bpm*4)
        self.current_beat = 0
        self.next_beat_time = 0.0

        self.playlist = playlist_test

        self.key_cooldowns = {k: 0.0 for k in self.ORIGINS_BINDS}
        self.input_cooldown = 0.25
        self.hit_window = 100

        self.hitbox_image = pygame.image.load(r"sprites\ph-master-hb.png").convert_alpha()
        self.score_line = BeatLine(self, (400, 900), self.hitbox_image, self.game.all_sprites)
        self.miss_line = pygame.Rect(200, 950, 400, 100)

        pygame.mixer.music.load(r'music\test1.mp3')
        pygame.mixer.music.set_volume(0.5)

    def update_beats(self, current_song_time):
        while self.current_beat < len(self.playlist) and current_song_time >= self.next_beat_time:
            self._spawn_current_beat()
            beat_count, _ = self.playlist[self.current_beat]
            self.next_beat_time += beat_count * self.beat_duration
            self.current_beat += 1

    def _spawn_current_beat(self):
        if self.current_beat >= len(self.playlist):
            return
        _, lanes = self.playlist[self.current_beat]
        current_time = pygame.mixer.music.get_pos() / 1000.0
        for i, active in enumerate(lanes):
            if active:
                self._spawn_TapNote(i, current_time)

    def _spawn_TapNote(self, origin, current_time):
        TapNote(self, origin, self.game.ph_image, (self.notes, self.game.all_sprites), current_time)

    def handle_input(self, key, current_time):
        if current_time < self.key_cooldowns[key]:
            return

        origin_idx = self.ORIGINS_BINDS.index(key)
        target_y = self.score_line.rect.centery
        closest_proj = None
        min_dist = float('inf')

        for proj in self.notes.sprites():
            if proj.origin == origin_idx:
                dist = abs(proj.hitbox_rect.centery - target_y)
                if dist < min_dist and dist <= self.hit_window:
                    min_dist = dist
                    closest_proj = proj

        if closest_proj:
            closest_proj.kill()
            self.game.score_master.judge(min_dist)
            self.key_cooldowns[key] = current_time + self.input_cooldown

    def check_misses(self):
        for proj in self.notes.sprites():
            if proj.hitbox_rect.bottom > self.miss_line.top:
                proj.kill()
                self.game.score_master.judge(-1)

class ScoreMaster:
    GRADES = {
        'perfect': {
            'hit_window': 40.0,
            'score': 50, 
            },
        'good': {
            'hit_window': 60.0,
            'score': 25, 
            },
        'normal': {
            'hit_window': 100.0,
            'score': 10, 
            },
        'miss': {
            'hit_window': -1.0,
            'score': 0, 
            },
        }
    
    COMBOS = {
        0: 1,
        10: 1.5,
        30: 2,
        50: 3,
    }

    def __init__(self, game):
        self.game = game
        self.score = 0
        self.combo_counter = 0
        self.combo_modifier = 1
        self.last_grade = ''

    def judge(self, distance):
        G = list(self.GRADES.items())
        G.sort(key = lambda x: x[1]['hit_window'])
        print(G)

        for grade in G:
            target_distance = grade[1]['hit_window']
            score = grade[1]['score']
            if distance <= float(target_distance):
                self.score += score * self.combo_modifier
                self.combo_counter += 1
                self.last_grade = grade[0]
                if score == 0:
                    self.combo_counter = 0
                break
                #print(distance, float(target_distance)) 
            
        
        #print(self.score, self.combo_modifier, distance)
        self._update_combo_modifier()

    def _update_combo_modifier(self):
        for threshold, multiplier in self.COMBOS.items():
            if self.combo_counter >= threshold:
                self.combo_modifier = multiplier
    
    def draw_score(self):
        #ВРЕМЕННО
        font = pygame.font.Font(None, 36)
        score = font.render(str(self.score), True, (0, 0, 0))
        game.screen.blit(score, (50, 50))
        modifier = font.render(str(self.combo_modifier), True, (0, 0, 0))
        game.screen.blit(modifier, (50, 100))
        modifier = font.render(str(self.last_grade), True, (0, 0, 0))
        game.screen.blit(modifier, (50, 150))



class Game:
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 1000))
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.note_master = NoteMaster(self)
        self.score_master = ScoreMaster(self)
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
                    if event.key in self.note_master.ORIGINS_BINDS:
                        self.note_master.handle_input(event.key, current_song_time)

            self.note_master.update_beats(current_song_time)

            for proj in self.note_master.notes.sprites():
                proj.move()

            self.note_master.check_misses()

            self.all_sprites.draw(self.screen)
            self.score_master.draw_score()
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000
            dt = max(0.001, min(0.1, dt))
            total_time += dt

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
