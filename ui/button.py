import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, color_normal=(180, 180, 180), color_hover=(160, 160, 169), color_pressed=(140, 140, 140), text_color=(40, 40, 40), border_color=(200, 200, 200), border_width=2, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_pressed = color_pressed
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width

        self.action = action 
        self.is_hovered = False
        self.is_pressed = False

        self._text_surface = self.font.render(self.text, True, self.text_color)
        self._text_rect = self._text_surface.get_rect(center=self.rect.center)

    def update(self, mouse_pos, mouse_buttons):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_pressed = self.is_hovered and mouse_buttons[0]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.action:
                    self.action()
                return True
            self.is_pressed = False
        return False

    def draw(self, screen):
        if self.is_pressed:
            color = self.color_pressed
        elif self.is_hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect,
                             width=self.border_width, border_radius=8)

        screen.blit(self._text_surface, self._text_rect)