import pygame
import random
from Test.TestModel import TestModel
from Test.TestView import TestView


class TestController:
    def __init__(self, user_id):
        pygame.init()
        self.original_screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.original_screen_size)
        pygame.display.set_caption("단어 테스트")
        self.font = pygame.font.SysFont("D2Coding", 32)
        self.view = TestView(self.screen, self.font)
        self.model = TestModel()
        self.running = True
        self.state = 'selecting_mode'
        self.selected_level = None
        self.current_word_index = 0
        self.score = 0
        self.game_mode = None
        self.words = []
        self.clock = pygame.time.Clock()
        self.user_id = user_id
        self.enter_event_handled = False
        self.background_color = 'white'
        self.answer_display_time = 0
        self.choice = None
        self.shuffle = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            current_time = pygame.time.get_ticks()
            if self.enter_event_handled and current_time - self.answer_display_time > 1000:
                self.background_color = 'white'
                self.enter_event_handled = False

            self.screen.fill(self.background_color)

            if self.state == 'selecting_mode':
                self.view.render_mode_selection()
            elif self.state == 'selecting_levels':
                self.view.render_level_selection(self.selected_level)
            else:
                self.render_test()

            pygame.display.update()
            self.clock.tick(30)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousedown(event)
        elif event.type == pygame.USEREVENT:
            self.handle_userevent(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self.enter_event_handled = False
        self.view.update_input_box(event)

    def handle_mousedown(self, event):
        if self.view.home_button.collidepoint(event.pos):
            self.reset_to_mode_selection()
            self.running = False
        elif self.state == 'selecting_mode':
            self.handle_mode_selection(event)
        elif self.state == 'selecting_levels':
            self.handle_level_selection(event)
        elif self.state == 'testing' and '객관식' in self.game_mode:
            self.handle_choice(event)

    def handle_mode_selection(self, event):
        for rect, mode in self.view.mode_buttons:
            if rect.collidepoint(event.pos):
                self.game_mode = mode
                self.state = 'selecting_levels'

    def handle_level_selection(self, event):
        for rect, level in self.view.level_buttons:
            if rect.collidepoint(event.pos):
                self.selected_level = level
                break
        if self.view.start_button.collidepoint(event.pos) and self.selected_level:
            self.start_test()

    def handle_choice(self, event):
        for rect, choice in self.view.choice_buttons:
            if rect.collidepoint(event.pos):
                self.view.box.text = choice
                self.enter_event_handled = False
                self.check_answer(choice)
                self.shuffle = True

    def handle_userevent(self, event):
        if event.name == 'enterEvent' and self.state == 'testing' and not self.enter_event_handled:
            user_input = event.text.strip()
            if user_input != '':
                self.check_answer(user_input)

    def reset_to_mode_selection(self):
        self.state = 'selecting_mode'
        self.current_word_index = 0
        self.score = 0
        self.words = []

    def start_test(self):
        self.state = 'testing'
        self.words = self.model.fetch_wordcards(
            limit=10,
            filter_levels=self.selected_level,
            user_id=self.user_id
        )
        pygame.display.set_mode((800, 600))

    def check_answer(self, user_input):
        if '한 -> 영' in self.game_mode:
            correct_answer = self.words[self.current_word_index][0]
        else:
            correct_answer = self.words[self.current_word_index][1]

        if user_input == correct_answer:
            self.score += 1
            self.view.show_answer('정답입니다!')
            self.model.delet_wrong_answer(self.user_id, self.words[self.current_word_index][0])
        else:
            self.model.save_wrong_answer(self.user_id, self.words[self.current_word_index][0])
            self.view.show_answer(correct_answer)

        self.current_word_index += 1
        self.view.box.text = ''
        self.view.box.hanText = ''
        self.enter_event_handled = True
        self.answer_display_time = pygame.time.get_ticks()

        if self.current_word_index >= len(self.words):
            self.running = False

    def render_test(self):
        if '객관식' in self.game_mode and self.shuffle and self.running:
            self.choice = self.model.fetch_wordcards(limit=3, exclude=self.words[self.current_word_index][0])
            # shuffle the choices
            self.choice.append(self.words[self.current_word_index])
            random.shuffle(self.choice)
            self.shuffle = False

        if self.current_word_index < len(self.words):
            self.view.render_word(
                self.game_mode,
                self.words[self.current_word_index],
                self.choice,
                self.current_word_index,
                len(self.words)
            )
            if '객관식' in self.game_mode:
                for event in pygame.event.get():
                    self.handle_event(event)

        else:
            self.view.render_score(self.score, len(self.words))
            self.current_word_index = 0
            pygame.display.update()
            pygame.time.wait(2000)
            self.running = False
            self.shuffle = False

