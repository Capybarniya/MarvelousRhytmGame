import pygame
from game_mods.game_mod import GameMode
from managers import LevelMaster, MusicMaster
from sprites import Sprite
from ui import UIDungeon
from settings import *

class DungeonMode(GameMode):
    def __init__(self, game):
        super().__init__(game)
        self.player_sprites = pygame.sprite.Group()
        self.level_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

        self.background_sprites = pygame.sprite.Group()
        self.background_upper_sprites = pygame.sprite.Group()

        background_img = self.game.asset_master.get_image(BACKGROUND_DUNGEON_IMAGE)
        Sprite((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), background_img, self.background_sprites)

        background_upper_img = self.game.asset_master.get_image(BACKGROUND_UPPER_DUNGEON_IMAGE)
        Sprite((background_upper_img.get_width()//2 + 2, background_upper_img.get_height()//2), background_upper_img, self.background_upper_sprites)

        self.level_master = LevelMaster(self, self.game.asset_master)
        self.music_master = MusicMaster(game.asset_master)
        self.ui = UIDungeon(self.level_master, self.game.asset_master, self.music_master)

        self.music_master.set_song_duration(60+17)

    def enter(self):
        self.level_master.generate_level()
        self.level_master.start()
        self.music_master.start_music(DUNGEON_MUSIC)
    
    def exit(self):
        self.level_master.cleanup()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in DUNGEON_BINDS and self.music_master.is_time_on_beat():
                dir = DUNGEON_BINDS[event.key]
                player = self.level_master.player
                
                if player.locked_by:
                    player.attempt_parry(dir)
                else:
                    player.move(dir)
            
    def _update_enemies(self, current_beat):
        for enemy in self.enemy_sprites:
            enemy.update(current_beat)  

    def update(self, dt):
        music_master = self.music_master
        music_master.update()
        
        if music_master.is_new_beat():
            player = self.level_master.player
            current_beat = music_master.current_beat
            
            player.update(current_beat)
            
            player.parry_attempted = False

            self.effect_sprites.update()
            self._update_enemies(current_beat)

        if music_master.check_if_time_over():
            exit_event = pygame.event.Event(GAME_OVER_EVENT)
            pygame.event.post(exit_event)
    
    def render(self, screen):
        self.background_sprites.draw(screen)
        self.level_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
        self.player_sprites.draw(screen)
        self.effect_sprites.draw(screen)
        self.background_upper_sprites.draw(screen)
        self.ui.draw(screen)