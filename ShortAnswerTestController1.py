import pygame
from pygame.locals import *
from ShortAnswerTestModel1 import ShortAnswerTestModel
from ShortAnswerTestView1 import ShortAnswerTestView
from hangulInputBox import HangulInputBox


class ShortAnswerTestController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption("Short Answer Test")

        self.model = ShortAnswerTestModel()
        self.view = ShortAnswerTestView(self.screen)
        self.running = True
        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.user_input = ""
        self.test_mode = None  # '한->영' or '영->한'

    def start_test(self, level, mode):
        self.questions = self.model.fetch_words(level)
        self.current_question_index = 0
        self.score = 0
        self.user_input = ""
        self.test_mode = mode
        self.run_test()

    def check_answer(self):
        question = self.questions[self.current_question_index]
        user_answer = self.user_input

        if self.test_mode == '한->영':
            correct_answer = question.word
        else:
            correct_answer = question.mean

        if user_answer.strip().lower() == correct_answer.strip().lower():
            self.score += 10

        self.user_input = ''
        self.view.input_box.hanText = ''
        self.current_question_index += 1

        if self.current_question_index >= 10 or self.current_question_index >= len(self.questions):
            self.view.display_result(self.score)
            pygame.time.wait(3000)  # 3초 대기
            self.running = False  # 프로그램 종료
        else:
            self.display_question()

    def display_home(self):
        self.view.display_home()

    def display_question(self):
        question = self.questions[self.current_question_index]
        if self.test_mode == '한->영':
            prompt = question.mean
        else:
            prompt = question.word
        self.view.display_question(prompt, self.user_input)

    def run_test(self):
        self.display_question()
        while self.running:
            keyEvent = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keyEvent = event
                    if event.key == pygame.K_RETURN:
                        print(f"User input: {self.user_input}")  # 입력된 전체 문자열 출력
                        self.check_answer()
                        self.user_input = ""  # 다음 입력을 위해 초기화
                elif event.type == MOUSEBUTTONDOWN:
                    for level, rect in self.view.level_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_level = level
                            self.display_home()  # 선택된 단계를 반영하기 위해 화면 갱신
                    for mode, rect in self.view.mode_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_mode = mode
                            self.display_home()  # 선택된 모드를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(event.pos) and self.view.selected_level and self.view.selected_mode:
                        self.start_test(self.view.selected_level, self.view.selected_mode)
                elif event.type == pygame.USEREVENT:
                    if event.name == 'enterEvent':
                        print(event.text)  # 입력된 전체 문자열 출력
                        self.check_answer()

            self.view.input_box.update(keyEvent)
            self.display_question()
        pygame.quit()

    def run(self):
        self.display_home()
        while self.running:
            keyEvent = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keyEvent = event
                    if event.key == pygame.K_RETURN:
                        print(f"User input: {self.user_input}")  # 입력된 전체 문자열 출력
                        self.user_input = ""  # 다음 입력을 위해 초기화
                elif event.type == MOUSEBUTTONDOWN:
                    for level, rect in self.view.level_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_level = level
                            self.display_home()  # 선택된 단계를 반영하기 위해 화면 갱신
                    for mode, rect in self.view.mode_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_mode = mode
                            self.display_home()  # 선택된 모드를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(event.pos) and self.view.selected_level and self.view.selected_mode:
                        self.start_test(self.view.selected_level, self.view.selected_mode)
                elif event.type == pygame.USEREVENT:
                    if event.name == 'enterEvent':
                        print(event.text)  # 입력된 전체 문자열 출력

            self.view.input_box.update(keyEvent)
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    controller = ShortAnswerTestController()
    controller.run()