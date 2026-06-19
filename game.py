import pygame
from managers import LevelMaster, MusicMaster, AssetMaster

class Game:
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((960, 1000))

        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.level_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

        self.asset_master = AssetMaster()


        self.level_master = LevelMaster(self)

        self.music_master = MusicMaster(self)

        
    def update_enemies(self):
        for enemy in self.enemy_sprites:
            if self.music_master.current_beat % enemy.speed == 0 and enemy.is_alive:
                enemy.behavior.get_next_action()
            
            if self.level_master.is_occupied_by_player(enemy.tile_pos):
                self.handle_player_defeat()

    def handle_player_defeat(self):
        #print("Игрок пойман! Игра окончена.")
        #pygame.mixer.music.stop()
        #self.running = False
        pass

    def run(self):
        pygame.mixer.music.play()
        dt = 0.1
        last_beat_processed = -1

        while self.running:
            self.screen.fill((255, 255, 255))
            current_song_time = pygame.mixer.music.get_pos() / 1000.0
            self.music_master.update_beats(current_song_time)

            if self.music_master.current_beat > last_beat_processed:
                self.effect_sprites.update()
                self.update_enemies()
                last_beat_processed = self.music_master.current_beat

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.level_master.player.BINDS and self.music_master.is_time_on_beat(current_song_time):
                        self.level_master.player.handle_input(event.key)
                        
                        for enemy in self.enemy_sprites:
                            if self.level_master.is_occupied_by_player(enemy.tile_pos):
                                self.handle_player_defeat()

            self.level_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.effect_sprites.draw(self.screen)
            #self.all_sprites.draw(self.screen)
            
            pygame.display.flip()
            
            dt = self.clock.tick(240) / 1000
            dt = max(0.001, min(0.1, dt))