import pygame


class View:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("로그인")
        self.font = pygame.font.SysFont("d2coding", 32)
        self.text_color = pygame.Color('black')
        self.register_button = pygame.Rect(350, 320, 130, 50)  # 회원가입 버튼 추가

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

    def draw_register_button(self):  # 회원가입 버튼 그리기
        pygame.draw.rect(self.screen, (0, 255, 0), self.register_button)
        self.draw_text('Register', self.register_button)

