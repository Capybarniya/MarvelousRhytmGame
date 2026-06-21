import pygame
from game_mods.game_state import GameState
from ui.button import Button
from settings import *

class MainMenuState(GameState):

    def __init__(self, game, state_machine):
        super().__init__(game, state_machine)

        self.title_font = pygame.font.Font(MAIN_FONT, 70)
        self.button_font = pygame.font.Font(MAIN_FONT, 56)

        self.bg_color = (42, 42, 42)
        self.accent_color = (180, 180, 180)

        button_width = 360
        button_height = 70
        button_spacing = 30
        buttons_x = (SCREEN_WIDTH - button_width) // 2
        buttons_y_start = SCREEN_HEIGHT // 2 + 40

        self.buttons = [
            Button(
                x=buttons_x,
                y=buttons_y_start,
                width=button_width,
                height=button_height,
                text="START",
                font=self.button_font,
                action=self._start_game,
            ),
            Button(
                x=buttons_x,
                y=buttons_y_start + button_height + button_spacing,
                width=button_width,
                height=button_height,
                text="EXIT",
                font=self.button_font,
                action=self._quit_game,
            ),
        ]

        self.logo_surface = None
        self.title_text = "ENTER THE BEATGEON"
        self._title_surface = self.title_font.render(
            self.title_text, True, self.accent_color
        )
        self._title_rect = self._title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )

    def enter(self):
        pygame.mouse.set_visible(True)

    def exit(self):
        pygame.mouse.set_visible(False)

    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._quit_game()
                return
            if event.key == pygame.K_RETURN:
                self._start_game()

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        for button in self.buttons:
            button.update(mouse_pos, mouse_buttons)

    def render(self, screen):
        screen.fill(self.bg_color)

        screen.blit(self._title_surface, self._title_rect)

        for button in self.buttons:
            button.draw(screen)

    def _start_game(self):
        from game_mods.playing_state import PlayingState
        self.state_machine.change_state(PlayingState)
        from game_mods.hint_state import HintState
        self.state_machine.push_state(HintState, (HINT_DUNGEON))

    def _quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))