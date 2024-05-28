import pygame
from pygame.locals import *
from ShortAnswerTestModel import ShortAnswerTestModel
from ShortAnswerTestView import ShortAnswerTestView

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

    def start_test(self, level):
        self.questions = self.model.fetch_words(level)
        self.current_question_index = 0
        self.score = 0
        self.user_input = ""
        self.run_test()

    def check_answer(self):
        correct_answer = self.questions[self.current_question_index].word
        if self.user_input.lower() == correct_answer.lower():
            self.score += 10
        self.user_input = ""
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
        question = self.questions[self.current_question_index].mean
        self.view.display_question(question, self.user_input)

    def run_test(self):
        self.display_question()
        while self.running:
            keyEvent = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    keyEvent = event
                    if event.key == K_RETURN:
                        self.check_answer()
                        self.display_question()
                elif event.type == MOUSEBUTTONDOWN:
                    for level, rect in self.view.level_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_level = level
                            self.display_home()  # 선택된 단계를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(event.pos) and self.view.selected_level:
                        self.start_test(self.view.selected_level)

                self.view.input_box.update(keyEvent)
                self.user_input = self.view.input_box.text

            pygame.display.update()
        pygame.quit()

    def run(self):
        self.display_home()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    for level, rect in self.view.level_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_level = level
                            self.display_home()  # 선택된 단계를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(event.pos) and self.view.selected_level:
                        self.start_test(self.view.selected_level)
        pygame.quit()

if __name__ == "__main__":
    controller = ShortAnswerTestController()
    controller.run()