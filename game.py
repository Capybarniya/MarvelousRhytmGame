import pygame
from managers import AssetMaster
from game_mods import GameStateMachine, MainMenuState
from settings import * 

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.asset_master = AssetMaster()

        self.state_machine = GameStateMachine(self)
        self.state_machine.push_state(MainMenuState)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_machine.handle_event(event)
            
            self.state_machine.update(dt)
            
            self.screen.fill((255, 255, 255))
            self.state_machine.render(self.screen)
            pygame.display.flip()
