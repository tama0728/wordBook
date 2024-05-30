import pygame
from pygame import Surface
from pygame.rect import Rect


class Popup:
    def __init__(self) -> None:
        self.popup_font = pygame.font.SysFont("d2coding", 32)
        self.popup_rect = Rect(200, 200, 240, 80)  # 팝업 메시지 박스 크기
        self.popup_color = pygame.Color('lightgray')  # 팝업 메시지 박스 색상
        self.popup_text_color = pygame.Color('black')  # 팝업 메시지 텍스트 색상 (변경됨)
        self.popup_visible = False
        self.popup_text = ""
        self.popup_timer = 0

    def show(self, message, timer=45, rect=None):
        if rect:
            self.popup_rect = rect
        self.popup_text = message
        self.popup_visible = True
        self.popup_timer = timer

    def hide(self):
        self.popup_visible = False

    def draw(self, screen):
        if self.popup_visible:
            popup_surface = Surface((self.popup_rect.width, self.popup_rect.height))
            popup_surface.fill(self.popup_color)
            popup_surface.set_alpha(200)
            text_surface = self.popup_font.render(self.popup_text, True, self.popup_text_color)
            text_rect = [(popup_surface.get_width() - text_surface.get_width()) // 2,
                         (popup_surface.get_height() - text_surface.get_height()) // 2]
            popup_surface.blit(text_surface, text_rect)
            screen.blit(popup_surface, self.popup_rect.topleft)
            if self.popup_timer > 0:
                self.popup_timer -= 1
            if self.popup_timer <= 0:
                self.hide()
