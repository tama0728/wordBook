import pygame
import random
import time
from Test.Short.ShortAnswerTestModel import ShortAnswerTestModel
from Test.Short.ShortAnswerTestView import ShortAnswerTestView


class ShortAnswerTestController:
    def __init__(self, user_id):  # user_id를 인자로 받음
        pygame.init()
        self.original_screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.original_screen_size)
        pygame.display.set_caption("단어 테스트")
        self.font = pygame.font.SysFont("D2Coding", 32)
        self.view = ShortAnswerTestView(self.screen, self.font)
        self.model = ShortAnswerTestModel()
        self.running = True
        self.selecting_mode = True
        self.selecting_levels = False
        self.selected_level = None
        self.current_word_index = 0
        self.score = 0
        self.game_mode = None
        self.words = []
        self.clock = pygame.time.Clock()
        self.user_id = user_id  # user_id 저장
        self.enter_event_handled = False  # 엔터 이벤트 처리를 위한 플래그
        self.background_color = 'white'
        self.answer_display_time = 0  # 배경 색 변경 시간 기록

    def run(self):
        while self.running:
            key_event = None
            start_button_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    key_event = event
                    if event.key == pygame.K_RETURN:
                        self.enter_event_handled = False
                    self.view.update_input_box(event)  # 입력 이벤트를 HangulInputBox에 전달
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.home_button.collidepoint(event.pos):
                        if self.selecting_levels:
                            self.selecting_levels = False
                            self.selecting_mode = True
                            pygame.display.set_mode(self.original_screen_size)  # 원래 창 크기로 변경
                        elif not self.selecting_mode and not self.selecting_levels:
                            self.selecting_levels = False
                            self.selecting_mode = True
                            self.current_word_index = 0
                            self.score = 0
                            self.words = []
                            pygame.display.set_mode(self.original_screen_size)  # 원래 창 크기로 변경
                        else:
                            self.running = False
                    if self.selecting_mode:
                        for rect, mode in self.view.mode_buttons:
                            if rect.collidepoint(event.pos):
                                self.game_mode = mode
                                self.selecting_mode = False
                                self.selecting_levels = True
                    elif self.selecting_levels:
                        for rect, level in self.view.level_buttons:
                            if rect.collidepoint(event.pos):
                                self.selected_level = level
                        start_rect = self.view.start_button
                        if start_rect.collidepoint(event.pos) and self.selected_level:
                            start_button_clicked = True
                            self.selecting_levels = False
                            filter_levels = []
                            if 'Level' in self.selected_level:
                                filter_levels = [int(self.selected_level.split(' ')[1])]
                            elif self.selected_level == 'Favorites':
                                filter_levels = None
                            elif self.selected_level == 'Wrong':
                                filter_levels = None
                            self.words = self.model.fetch_wordcards(limit=10, filter_levels=filter_levels,
                                                                    user_id=self.user_id,
                                                                    only_favorites=(self.selected_level == 'Favorites'),
                                                                    only_wrong=(self.selected_level == 'Wrong'))
                            pygame.display.set_mode((800, 600))  # 창 크기 변경

                if event.type == pygame.USEREVENT and not self.enter_event_handled:
                    if event.name == 'enterEvent' and not (self.selecting_mode or self.selecting_levels):
                        user_input = event.text.strip()
                        print(f"입력한 값: {user_input}")
                        if '한 -> 영' in self.game_mode:
                            correct_answer = self.words[self.current_word_index].word
                        elif '영 -> 한' in self.game_mode:
                            correct_answer = self.words[self.current_word_index].mean
                        if user_input == correct_answer:
                            self.score += 1
                            print("정답!")

                        else:
                            print("오답!")
                            self.model.save_wrong_answer(self.user_id,
                                                         self.words[self.current_word_index].word)  # 틀린 답 저장

                        self.current_word_index += 1
                        self.view.box.text = ''
                        self.view.box.hanText = ''
                        self.enter_event_handled = True
                        self.answer_display_time = pygame.time.get_ticks()
                        if self.current_word_index >= len(self.words):
                            self.running = False

            current_time = pygame.time.get_ticks()
            if self.enter_event_handled and current_time - self.answer_display_time > 1000:  # 1초 후 다음 문제로 이동
                self.background_color = 'white'
                self.enter_event_handled = False

            self.screen.fill(self.background_color)

            if self.selecting_mode:
                self.view.render_mode_selection()
            elif self.selecting_levels:
                self.view.render_level_selection(self.selected_level)
            else:
                if self.current_word_index < len(self.words):
                    self.view.render_word(self.game_mode, self.words[self.current_word_index], '주관식' in self.game_mode,
                                          self.current_word_index, len(self.words))
                else:
                    self.view.render_score(self.score, len(self.words))
                    pygame.display.update()
                    pygame.time.wait(2000)  # 2초 동안 점수 표시
                    self.running = False

            pygame.display.update()
            self.clock.tick(30)
