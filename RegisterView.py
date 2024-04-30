import pygame


class RegisterView:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("회원가입")
        self.font = pygame.font.SysFont("d2coding", 32)
        self.text_color = pygame.Color('black')

    def draw_text(self, text, rect, where='center'):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        if where == 'center':
            text_rect.center = rect.center
        elif where == 'left_out':
            text_rect.centery = rect.centery
            text_rect.x = rect.x - text_rect.width - 3
        elif where == 'left_in':
            text_rect.centery = rect.centery
            text_rect.x = rect.left + 3
        self.screen.blit(text_surface, text_rect)
