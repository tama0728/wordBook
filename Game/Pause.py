import pygame

from Game.GameRectangle import Rectangle

WHITE = (255, 255, 255)


class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.overlay_visible = False

        # "계속" 버튼 사각형 정의
        self.continue_button = Rectangle(self.screen_width - 220, self.screen_height - 240, 200, 100, color=WHITE, border_radius=10)
        self.continue_button.set_text("계속", font_size=24)

        # "종료" 버튼 사각형 정의
        self.quit_button = Rectangle(self.screen_width - 220, self.screen_height - 120, 200, 100, color=WHITE, border_radius=10)
        self.quit_button.set_text("종료", font_size=24)

    def draw(self):
        if self.overlay_visible:
            # 불투명한 레이어 그리기
            overlay_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 128))  # 검은색 불투명 레이어
            self.screen.blit(overlay_surface, (0, 0))

            # "계속" 버튼 그리기
            self.continue_button.draw(self.screen)

            # "종료" 버튼 그리기
            self.quit_button.draw(self.screen)

    def set_overlay_visible(self, visible):
        self.overlay_visible = visible
