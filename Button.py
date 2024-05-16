import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


class Button:
    def __init__(self, rect, text, color=GRAY):
        self.rect = rect
        self.color = color
        self.dim = False
        self.text = text
        self.font = pygame.font.SysFont("d2coding", 30)

    def draw(self, surface):
        if self.dim:
            pygame.draw.rect(surface, self.set_dim(), self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_collide(self, pos):
        return self.rect.collidepoint(pos)

    def set_active(self):
        self.dim = True

    def set_inactive(self):
        self.dim = False

    def set_dim(self):
        return self.color[0] // 2, self.color[1] // 2, self.color[2] // 2

    def is_hover(self, pos):
        if self.is_collide(pos):
            self.set_active()
        else:
            self.set_inactive()