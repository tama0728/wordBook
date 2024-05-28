import pygame
import sys
from Game.Pause import Pause

# 게임 컨트롤러 (입력 처리 및 게임 로직 연결)
class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.pause = Pause

    def handle_event(self, event):
        # 우측 상탄 X표 눌릴 시 게임 종료
        if event.type == pygame.QUIT:
            # 게임 종료
            pygame.quit()
            sys.exit()
        # 마우스가 클릭 될 때
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # "계속" 버튼이 눌릴 경우 ESC 상태 풀기
            if self.view.overlay_visible and self.view.pause.continue_button.collidepoint(pos):
                self.view.toggle_overlay()  # 오버레이 해제
                self.model.toggle_card_selection()  # 카드 선택 상태 토글
                self.view.draw()  # 화면 다시 그리기
            # "종료" 버튼이 눌릴 시 게임 종료
            if self.view.overlay_visible and self.view.pause.quit_button.collidepoint(pos):
                return False
            # Home 버튼이 눌릴 시 게임 종료
            elif pygame.Rect(self.view.screen_width - 70, self.view.screen_height - 70, 50, 50).collidepoint(pos):
                return False
            # 카드 선택
            else:
                for i, card in enumerate(self.model.cards):
                    x = (self.view.screen_width - (6 * self.view.card_width + 5 * self.view.margin)) // 2 + (i % 6) * (self.view.card_width + self.view.margin)
                    y = self.view.screen_height - self.view.margin - ((i // 6) + 1) * (self.view.card_height + self.view.margin) - 50
                    if pygame.Rect(x, y, self.view.card_width, self.view.card_height).collidepoint(pos):
                        if not self.model.disable_card_selection:  # 카드 선택이 활성화된 경우에만 동작
                            if self.model.first_card is None:  # 첫 번째 카드를 선택한 경우
                                if self.model.flip_card(i):
                                    self.view.draw()
                                    break  # 다음 카드를 선택할 수 없도록 종료
                            elif self.model.second_card is None:  # 두 번째 카드를 선택한 경우
                                if i != self.model.first_card:  # 같은 카드를 다시 선택한 경우는 무시
                                    if self.model.flip_card(i):
                                        self.view.draw()
                                        pygame.time.wait(500)
                                        self.model.check_match()
                                        break  # 다음 카드를 선택할 수 없도록 종료
        #카드 눌릴 때
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.view.toggle_overlay()
                self.model.toggle_card_selection()  # 카드 선택 상태 토글
                self.view.draw()  # 화면 다시 그리기

        return True