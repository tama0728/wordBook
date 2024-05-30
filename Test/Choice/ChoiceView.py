import pygame

from View import View
from Api.Button import Button


class ChoiceView:
    def __init__(self, view: View):
        self.view = view
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("2x2 Button Grid with Title")
        self.vuBtnWord = Button(pygame.Rect(300, 50, 200, 50), "english Word", (181, 223, 213))

        # 버튼 배열 생성
        self.vuBtnsWord = []
        button_width = 350
        button_height = 150
        padding = 40
        for row in range(2):
            for col in range(2):
                x = col * (button_width + padding) + 30
                y = row * (button_height + padding) + 150
                btn = Button(pygame.Rect(x, y, button_width, button_height), "", (200, 200, 200))
                self.vuBtnsWord.append(btn)
                # rs_words에서 뜻(mean)만 가져와서 버튼 텍스트로 설정

        # 현재 페이지 표시를 위한 텍스트 설정
        self.font = pygame.font.SysFont("d2coding", 20)

    def draw(self, current_page):
        self.screen.fill((255, 255, 255))
        self.vuBtnWord.draw(self.screen)
        for btn in self.vuBtnsWord:
            btn.draw(self.screen)

        # 현재 페이지 표시
        text_surface = self.font.render(f"{current_page}/20", True, (0, 0, 0))
        text_rect = text_surface.get_rect(bottomleft=(20, 580))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
