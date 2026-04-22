import pygame 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, master, origin, sprite):
        super().__init__()
        self.image = sprite
        self.origin = origin
        pos = master.ORIGINS[origin]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-8, -8)
        
    def move(self, y, dt):
        self.hitbox_rect.y += y * dt
        self.rect.center = self.hitbox_rect.center

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

class ProjectileMaster:
    ORIGINS = [(200, 0), (300, 0), (400, 0), (500, 0), (600, 0)]
    ORIGINS_BINDS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]

    def __init__(self):
        self.x = 200
        self.y = 0
        self.projectiles = pygame.sprite.Group()
        self.last_beat = 0
        self.hitbox_rect = pygame.Rect(150, 850, 1000, 500)

    def init_song(self):
        pass

    def beat(self):
        self.spawn_projectile(0)
        self.spawn_projectile(1)
        self.spawn_projectile(2)
        self.spawn_projectile(3)
        self.spawn_projectile(4)

    def spawn_projectile(self, origin):
        projectile = Projectile(self, origin, ph_image)
        self.projectiles.add(projectile)
    
pygame.init()

screen = pygame.display.set_mode((800, 1000))

ph_image = pygame.image.load(r"sprites\ph-1.png").convert()
ph_image = pygame.transform.scale(ph_image, (ph_image.get_width() * 2, ph_image.get_height() * 2))

running = True
clock = pygame.time.Clock()
Master = ProjectileMaster()
d_time = 0.1
total_time = 0

BEAT_EVENT = pygame.event.custom_type()
beat_event = pygame.event.Event(BEAT_EVENT, {'sprite': pygame.sprite.Sprite}) 

while running:
    screen.fill((255, 255, 255))

    for sprite in Master.projectiles.sprites():
        if Master.hitbox_rect.colliderect(sprite.hitbox_rect): 
            #print(sprite.hitbox_rect.center)
            beat_event = pygame.event.Event(BEAT_EVENT, {'sprite': sprite})  
            pygame.event.post(beat_event)

    if total_time - 1 >= Master.last_beat: 
        Master.beat()
        Master.last_beat = total_time
    for sprite in Master.projectiles.sprites(): sprite.move(400, d_time)
    Master.projectiles.draw(screen)

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False
        if event.type == BEAT_EVENT:
            for i in range(len(Master.ORIGINS)):
                if event.sprite.origin == i and keys[Master.ORIGINS_BINDS[i]]:
                    event.sprite.kill()



    pygame.display.flip()

    d_time = clock.tick(120) / 1000
    d_time = max(0.001, min(0.1, d_time))
    total_time += d_time


pygame.quit()