import pygame
import random
from ShortAnswerTestModel1 import ShortAnswerTestModel
from ShortAnswerTestView1 import ShortAnswerTestView

class ShortAnswerTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("단어 테스트")
        self.font = pygame.font.SysFont("D2Coding", 32)
        self.view = ShortAnswerTestView(self.screen, self.font)
        self.model = ShortAnswerTestModel()
        self.running = True
        self.selecting_mode = True
        self.selecting_levels = False
        self.selected_levels = []
        self.current_word_index = 0
        self.score = 0
        self.game_mode = None
        self.words = []
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            key_event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    key_event = event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.selecting_mode:
                        for rect, mode in self.view.mode_buttons:
                            if rect.collidepoint(event.pos):
                                self.game_mode = mode
                                self.selecting_mode = False
                                self.selecting_levels = True
                    elif self.selecting_levels:
                        for rect, level in self.view.level_buttons:
                            if rect.collidepoint(event.pos):
                                if level in self.selected_levels:
                                    self.selected_levels.remove(level)
                                else:
                                    self.selected_levels.append(level)
                        if self.selected_levels:
                            start_text = self.font.render("Start", True, 'black')
                            start_rect = start_text.get_rect(center=(400, 450))
                            self.screen.blit(start_text, start_rect)
                            if start_rect.collidepoint(event.pos):
                                self.selecting_levels = False
                                self.words = self.model.fetch_wordcards(limit=10, filter_levels=self.selected_levels)
                if event.type == pygame.USEREVENT and not (self.selecting_mode or self.selecting_levels):
                    if event.name == 'enterEvent':
                        user_input = event.text.strip()
                        print(f"입력한 값: {user_input}")
                        if '한->영' in self.game_mode:
                            correct_answer = self.words[self.current_word_index].word
                        elif '영->한' in self.game_mode:
                            correct_answer = self.words[self.current_word_index].mean
                        if user_input == correct_answer:
                            self.score += 1
                            print("정답!")
                        else:
                            print("오답!")
                        self.current_word_index += 1
                        self.view.box.text = ''
                        self.view.box.hanText = ''
                        if self.current_word_index >= len(self.words):
                            self.running = False

            self.screen.fill('white')

            if self.selecting_mode:
                self.view.render_mode_selection()
            elif self.selecting_levels:
                self.view.render_level_selection(self.selected_levels)
                if self.selected_levels:
                    start_text = self.font.render("Start", True, 'black')
                    start_rect = start_text.get_rect(center=(400, 450))
                    self.screen.blit(start_text, start_rect)
                    if event.type == pygame.MOUSEBUTTONDOWN and start_rect.collidepoint(event.pos):
                        self.selecting_levels = False
                        self.words = self.model.fetch_wordcards(limit=10, filter_levels=self.selected_levels)
            else:
                if self.current_word_index < len(self.words):
                    self.view.render_word(self.game_mode, self.words[self.current_word_index], '주관식' in self.game_mode)
                else:
                    self.view.render_score(self.score, len(self.words))

            pygame.display.update()
            self.clock.tick(30)

if __name__ == "__main__":
    controller = ShortAnswerTest()
    controller.run()
    pygame.quit()