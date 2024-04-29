import pygame


class View:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("로그인")
        self.font = pygame.font.Font("malgungothic", 32)
        self.text_color = pygame.Color('black')
        self.register_button = pygame.Rect(350, 320, 130, 50)  # 회원가입 버튼 추가
        self.popup_font = pygame.font.Font("malgungothic", 24)  # 팝업 메시지 폰트
        self.popup_rect = pygame.Rect(200, 200, 240, 80)  # 팝업 메시지 박스 크기
        self.popup_color = pygame.Color('lightgray')  # 팝업 메시지 박스 색상
        self.popup_text_color = pygame.Color('black')  # 팝업 메시지 텍스트 색상
        self.popup_visible = False
        self.popup_text = ""
        self.popup_timer = 0

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

    def show_popup(self, message, timer=45):
        self.popup_text = message
        self.popup_visible = True
        self.popup_timer = timer

    def hide_popup(self):
        self.popup_visible = False

    def draw_popup(self):
        if self.popup_visible:
            popup_surface = pygame.Surface((self.popup_rect.width, self.popup_rect.height))
            popup_surface.fill(self.popup_color)
            popup_surface.set_alpha(200)
            text_surface = self.popup_font.render(self.popup_text, True, self.popup_text_color, self.popup_color)
            text_rect = text_surface.get_rect(center=self.popup_rect.center)
            popup_surface.blit(text_surface, [0,0])
            self.screen.blit(popup_surface, self.popup_rect.topleft)
            if self.popup_timer > 0:
                self.popup_timer -= 1
            if self.popup_timer <= 0:
                self.hide_popup()
