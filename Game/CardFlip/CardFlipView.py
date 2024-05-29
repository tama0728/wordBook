import pygame
import os
from Game.GameRectangle import Rectangle
from Game.Pause import Pause

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
LIGHTRED = (255, 200, 200)


# 게임 뷰 (화면 그리기)
class CardFlipView:
    def __init__(self, model):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # 화면을 중앙에 배치
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.model = model
        self.screen_width, self.screen_height = self.screen.get_size()  # 화면의 너비와 높이 가져오기
        self.card_width = 120
        self.card_height = 80
        self.margin = 15
        self.overlay_visible = False  # 불투명한 레이어 표시 여부
        self.pause = Pause(self.screen)
        self.homeButton = Rectangle(self.SCREEN_WIDTH - 70, self.screen_height - 70, 50, 50)

    def toggle_overlay(self):
        self.overlay_visible = not self.overlay_visible

    def draw(self):
        # 화면을 흰색으로 채우기
        self.screen.fill(WHITE)
        # 화면에 카드 표시
        for i, card in enumerate(self.model.cards):
            # 카드의 위치 계산
            x = (self.screen_width - (6 * self.card_width + 5 * self.margin)) / 2 + (i % 6) * (
                        self.card_width + self.margin)
            y = self.screen_height - self.margin - ((i // 6) + 1) * (self.card_height + self.margin) - 50
            if card.state == 'hidden':
                rect_back = Rectangle(x, y, self.card_width, self.card_height, color=GRAY, border_radius=10)
                rect_back.draw(self.screen)
            elif card.state == 'shown':
                rect = Rectangle(x, y, self.card_width, self.card_height, color=LIGHTRED, border_radius=10)
                rect.set_text(str(card.value), text_color=BLACK, font_size=20)
                rect.draw(self.screen)
            elif card.state == 'matched':
                pass
            current_dir = os.path.dirname(__file__)
            self.homeButton.set_image(os.path.join(current_dir, 'assets', 'home.png'))
            self.homeButton.draw(self.screen)

        # 현재 경과 시간 표시
        if not self.overlay_visible:
            current_time = self.model.get_elapsed_time()
            minutes = current_time // 60
            seconds = current_time % 60
            time_text = f"{int(minutes):02d}:{int(seconds):02d}"  # 시간을 문자열로 변환
            time_rect = Rectangle(self.screen_width / 2 - 100, 20, 200, 70, GREEN, 10)
            time_rect.set_text(time_text, font_size=50)
            time_rect.draw(self.screen)

        # ESC가 눌렸을 때
        if self.overlay_visible:
            self.pause.set_overlay_visible(True)
            self.pause.draw()

        # 화면 업데이트
        pygame.display.flip()
