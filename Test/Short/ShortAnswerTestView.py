import pygame
# from Api.hangulInputBox import HangulInputBox
from Api.Input import Input
import os
from View import View

class ShortAnswerTestView:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        # self.box = HangulInputBox('D2Coding', 32, 14, 'black', 'gray')
        self.box = Input("", self, pygame.Rect(0, 0, 0, 0))
        self.box.rect.center = (100, 200)  # 텍스트 입력창 위치 조정
        self.modes = ['영 -> 한\n객관식', '한 -> 영\n객관식', '영 -> 한\n주관식', '한 -> 영\n주관식']
        self.levels = ['Level 1', 'Level 2', 'Level 3', 'Favorites', 'Wrong']
        self.mode_buttons = self.create_buttons(self.modes, 2, 2)
        self.level_buttons = self.create_buttons(self.levels, 1, 5)
        self.start_button = pygame.Rect(350, 500, 100, 50)
        self.home_button = pygame.Rect(700, 500, 80, 80)

        # 이미지 로드
        current_dir = os.path.dirname(os.path.abspath(__file__))
        checkbox_checked_path = os.path.join(current_dir, "../../Images/checkbox_unchecked.png")
        checkbox_unchecked_path = os.path.join(current_dir, "../../Images/checkbox_checked.png")
        home_path = os.path.join(current_dir, "../../Images/home.png")

        self.checkbox_checked = pygame.image.load(checkbox_checked_path).convert_alpha()
        self.checkbox_checked = pygame.transform.scale(self.checkbox_checked, (30, 30))
        self.checkbox_unchecked = pygame.image.load(checkbox_unchecked_path).convert_alpha()
        self.checkbox_unchecked = pygame.transform.scale(self.checkbox_unchecked, (30, 30))
        self.home_icon = pygame.image.load(home_path).convert_alpha()
        self.home_icon = pygame.transform.scale(self.home_icon, (80, 80))

    def create_buttons(self, items, cols, rows):
        buttons = []
        screen_width, screen_height = self.screen.get_size()
        button_width = screen_width // (cols + 1)
        button_height = screen_height // (rows + 3)
        x_margin = (screen_width - (cols * button_width)) // (cols + 1)
        y_margin = (screen_height - (rows * button_height)) // (rows + 2)

        for i, item in enumerate(items):
            row = i % rows
            col = i // rows
            x = x_margin + col * (button_width + x_margin)
            y = y_margin + row * (button_height + y_margin)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((rect, item))
        return buttons

    def render_mode_selection(self):
        self.screen.fill('white')
        for rect, mode in self.mode_buttons:
            pygame.draw.rect(self.screen, (0, 128, 255), rect, border_radius=10)  # 진한 파란색 배경과 둥근 모서리
            pygame.draw.rect(self.screen, (255, 255, 255), rect.inflate(-6, -6), border_radius=10)  # 흰색 안쪽 배경
            lines = mode.split('\n')
            for idx, line in enumerate(lines):
                mode_text = self.font.render(line, True, 'black')
                mode_text_rect = mode_text.get_rect(center=(rect.centerx, rect.centery - 10 + idx * 20))  # 텍스트 두 줄 배치
                self.screen.blit(mode_text, mode_text_rect)
        self.screen.blit(self.home_icon, self.home_button)

    def render_level_selection(self, selected_level):
        self.screen.fill('white')
        for rect, level in self.level_buttons:
            image = self.checkbox_checked if level == selected_level else self.checkbox_unchecked
            self.screen.blit(image, rect.topleft)
            level_text = self.font.render(level, True, 'black')
            level_text_rect = level_text.get_rect(midleft=(rect.x + 40, rect.centery))
            self.screen.blit(level_text, level_text_rect)
        if selected_level:
            pygame.draw.rect(self.screen, (173, 216, 230), self.start_button, border_radius=10)
            start_text = self.font.render("Start", True, 'black')
            start_rect = start_text.get_rect(center=self.start_button.center)
            self.screen.blit(start_text, start_rect)
        self.screen.blit(self.home_icon, self.home_button)

    def render_word(self, game_mode, word, is_subjective, current_index, total_words):
        self.screen.fill('white')

        # 하늘색 큰 사각형
        rect = pygame.Rect(150, 100, 500, 250)
        pygame.draw.rect(self.screen, (173, 216, 230), rect, border_radius=10)

        # 단어 표시
        display_text = word.mean if '한 -> 영' in game_mode else word.word
        word_text = self.font.render(display_text, True, 'black')
        word_text_rect = word_text.get_rect(center=(rect.centerx, rect.centery))
        self.screen.blit(word_text, word_text_rect)

        # 문제 번호 표시
        progress_text = self.font.render(f"{current_index + 1}/{total_words}", True, 'black')
        progress_text_rect = progress_text.get_rect(bottomright=(rect.right - 10, rect.bottom - 10))
        self.screen.blit(progress_text, progress_text_rect)

        # 텍스트 입력창
        self.box.rect.midtop = (330, 400)  # slightly move the text input box to the left
        self.box.rect.width = 300  # 텍스트 입력창 너비 조정
        # self.box.update(None)  # 화면에 그리기 위해 update 호출
        self.box.draw(self.screen)
        self.screen.blit(self.box.image, self.box.rect)

        self.screen.blit(self.home_icon, self.home_button)

    def render_score(self, score, total):
        self.screen.fill('white')
        score_text = self.font.render(f"점수: {score}/{total}", True, 'black')
        score_text_rect = score_text.get_rect(center=(400, 300))
        self.screen.blit(score_text, score_text_rect)

    def update_input_box(self, event):
        self.box.update(event)
