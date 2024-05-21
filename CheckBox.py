import pygame


class CheckBox:
    def __init__(self, text, view, rect):
        self.text = text
        self.view = view
        self.rect = rect
        self.checked = False

    def draw(self):
        pygame.font.SysFont("d2coding", 2)
        pygame.draw.rect(self.view.screen, (0, 0, 0), self.rect, 2)

        if self.checked:
            pygame.draw.line(self.view.screen, (0, 0, 0), self.rect.topleft, self.rect.bottomright)
            pygame.draw.line(self.view.screen, (0, 0, 0), self.rect.topright, self.rect.bottomleft)
        self.view.draw_text(self.text, self.rect, 'left_out', 20)

    def is_collide(self, pos):
        return self.rect.collidepoint(pos)

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False
