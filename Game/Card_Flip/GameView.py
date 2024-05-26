import pygame
import os
from Game.GameRectangle import Rectangle
from Game.Pause import Pause

# 색상 정의
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# 게임 뷰 (화면 그리기)
class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.screen_width, self.screen_height = self.screen.get_size()  # 화면의 너비와 높이 가져오기
        self.card_width = 120
        self.card_height = 80
        self.margin = 15
        self.overlay_visible = False  # 불투명한 레이어 표시 여부
        self.pause = Pause(self.screen, self.screen_width, self.screen_height)
        self.homeButton = Rectangle(self.screen_width-70, self.screen_height-70, 50, 50)
        # 계속 버튼과 종료 버튼의 사각형 및 텍스트
        #self.continue_rect = pygame.Rect(self.screen_width - 250, self.screen_height - 220, 200, 80)
        #self.quit_rect = pygame.Rect(self.screen_width - 250, self.screen_height - 120, 200, 80)


    def toggle_overlay(self):
        self.overlay_visible = not self.overlay_visible

    def draw(self):
        # 화면을 흰색으로 채우기
        self.screen.fill(WHITE)
        # 화면에 카드 표시
        for i, card in enumerate(self.model.cards):
            # 카드의 위치 계산
            #x = self.margin + (i % 6) * (self.card_width + self.margin)
            x = (self.screen_width - (6 * self.card_width + 5 * self.margin)) / 2 + (i % 6) * (self.card_width + self.margin)
            #y = self.margin + (i // 6) * (self.card_height + self.margin)
            y = self.screen_height - self.margin - ((i // 6) + 1) * (self.card_height + self.margin) - 50
            if card.state == 'hidden':
                # 숨겨진 카드는 card_back 이미지로 그리기
                #self.screen.blit(self.card_back, (x, y))
                current_dir = os.path.dirname(__file__)
                rect_with_image = Rectangle(x, y, self.card_width, self.card_height)
                rect_with_image.set_image(os.path.join(current_dir, 'assets', 'card_back.jpg'))
                rect_with_image.draw(self.screen)
            elif card.state == 'shown':
                # 보이는 카드는 녹색 사각형과 값 텍스트로 그리기
                #pygame.draw.rect(self.screen, GREEN, (x, y, self.card_width, self.card_height))
                #value_text = pygame.font.SysFont("malgungothic", 20).render(str(card.value), True, WHITE)
                #self.screen.blit(value_text, (x + (self.card_width - value_text.get_width()) // 2, y + (self.card_height - value_text.get_height()) // 2))
                rect = Rectangle(x, y, self.card_width, self.card_height, color=GRAY)
                rect.set_text(str(card.value), text_color=WHITE, font_size=20)
                rect.draw(self.screen)
            elif card.state == 'matched':
                # 맞춘 카드는 빨간색 사각형으로 그리기
                #pygame.draw.rect(self.screen, RED, (x, y, self.card_width, self.card_height))
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
            time_rect = Rectangle(self.screen_width/2-100, 20, 200, 70, GREEN, 10)
            time_rect.set_text(time_text, font_size = 50)
            time_rect.draw(self.screen)

        # ESC가 눌렸을 때
        if self.overlay_visible:
            self.pause.set_overlay_visible(True)
            self.pause.draw()

        # 화면 업데이트
        pygame.display.flip()