import pygame

from trashbin.playlists import playlist_test

class Game:   
    def run(self):

        while self.running:
            
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000
            dt = max(0.001, min(0.1, dt))
            total_time += dt

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
