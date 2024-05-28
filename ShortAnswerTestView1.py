import pygame
from hangulInputBox import HangulInputBox

class ShortAnswerTestView:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.box = HangulInputBox('NanumBarunGothic.ttf', 32, 25, 'black', 'gray')
        self.box.rect.center = (400, 450)
        self.modes = ['영->한'+"\n"+'주관식', '한->영' +"\n"+'주관식', '영->한'+"\n"+'객관식', '한->영'+"\n"+'객관식']
        self.levels = [1, 2, 3]
        self.mode_buttons = self.create_buttons(self.modes, 2, 2)
        self.level_buttons = self.create_buttons(self.levels, 1, 3)
        self.start_button = pygame.Rect(350, 500, 100, 50)

    def create_buttons(self, items, cols, rows):
        buttons = []
        for i, item in enumerate(items):
            row = i // cols
            col = i % cols
            rect = pygame.Rect((200 + col * 200, 150 + row * 100), (250, 50))
            buttons.append((rect, item))
        return buttons

    def render_mode_selection(self):
        self.screen.fill('white')
        for rect, mode in self.mode_buttons:
            pygame.draw.rect(self.screen, 'skyblue', rect)
            mode_text = self.font.render(mode, True, 'black')
            mode_text_rect = mode_text.get_rect(center=rect.center)
            self.screen.blit(mode_text, mode_text_rect)

    def render_level_selection(self, selected_levels):
        self.screen.fill('white')
        for rect, level in self.level_buttons:
            color = 'green' if level in selected_levels else 'skyblue'
            pygame.draw.rect(self.screen, color, rect)
            level_text = self.font.render(f"Level {level}", True, 'black')
            level_text_rect = level_text.get_rect(center=rect.center)
            self.screen.blit(level_text, level_text_rect)
        if selected_levels:
            start_text = self.font.render("Start", True, 'black')
            start_rect = start_text.get_rect(center=self.start_button.center)
            pygame.draw.rect(self.screen, 'skyblue', self.start_button)
            self.screen.blit(start_text, start_rect)

    def render_word(self, game_mode, word, is_subjective):
        self.screen.fill('white')
        rect = pygame.Rect(200, 150, 400, 200)
        pygame.draw.rect(self.screen, 'skyblue', rect)
        display_text = word.mean if '한->영' in game_mode else word.word
        word_text = self.font.render(display_text, True, 'black')
        word_text_rect = word_text.get_rect(center=rect.center)
        self.screen.blit(word_text, word_text_rect)
        if is_subjective:
            self.box.rect.midtop = (400, 350)
            self.screen.blit(self.box.image, self.box.rect)
        else:
            # 객관식 선택지 표시
            pass

    def render_score(self, score, total):
        self.screen.fill('white')
        score_text = self.font.render(f"점수: {score}/{total}", True, 'black')
        score_text_rect = score_text.get_rect(center=(400, 300))
        self.screen.blit(score_text, score_text_rect)

    def update_input_box(self, event):
        self.box.update(event)