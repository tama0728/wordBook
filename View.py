import pygame
import os

class View:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1' # 화면을 중앙에 배치
        self.WIDTH, self.HEIGHT = 640, 480
        # self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pygame.font.SysFont("d2coding", 32)
        self.text_color = pygame.Color('black')
        pygame.key.set_repeat(500, 50)

    def draw_text(self, text, rect, where='center', font_size=32):
        self.font = pygame.font.SysFont("d2coding", font_size)
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

    def set_display_size(self, width=640, height=480):
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pygame.font.SysFont("d2coding", 32)
        self.text_color = pygame.Color('black')
        pygame.key.set_repeat(500, 50)