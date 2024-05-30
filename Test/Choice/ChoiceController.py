import pygame
import sys

from Test.Choice.ChoiceModel import ChoiceModel
from Test.Choice.ChoiceView import ChoiceView
from View import View
from Api.Popup import Popup
from Api.Button import Button  # Assuming you have a Button class in this module


class ChoiceController:
    def __init__(self):
        self.view = View()
        self.vuSelWordView = SelWordView(self.view)
        self.selwordModel = SelWordModel()
        self.mode = "eng_to_kor"
        self.correct_answer = None
        self.previous_word = None
        self.total_questions = 20
        self.correct_answers = 0
        self.current_page = 0  # 현재 페이지 초기값

    def load_new_question(self):
        if self.total_questions > 0:
            self.aQaA = self.selwordModel.generate_question(self.mode)
            self.correct_answer = self.aQaA['answer']
            self.previous_word = self.aQaA['question']
        # 문제
            self.vuSelWordView.vuBtnWord.text = self.aQaA['question']

        # 4지선다 버튼
            for i in range(len(self.vuSelWordView.vuBtnsWord)):
                if i < len(self.aQaA['choices']):
                    self.vuSelWordView.vuBtnsWord[i].text = self.aQaA['choices'][i]
                    self.vuSelWordView.vuBtnsWord[i].color = (222, 232, 241)  # Reset button color
            self.total_questions -= 1 # 문제 풀이 횟수 감소
            self.current_page += 1 # 다음 페이지
        else:
            self.show_score()

    def run(self):
        pygame.init()
        screen = self.vuSelWordView.screen
        # 화면 크기 설정
        screen_width = 800
        screen_height = 600
        pygame.display.set_caption("2x2 Button Grid with Title")

        # 색상 정의
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)

        # 버튼 크기 및 위치 설정
        button_width = 200
        button_height = 100
        button_margin = 80

        font = pygame.font.SysFont("d2coding", 24)

        self.load_new_question()  # Load the initial question

        # 버튼 배열 위치(rect2D) 생성
        rcButtons = []
        bi = 0
        for i in range(2):
            for j in range(2):
                x = j * (button_width + button_margin) + button_margin
                y = i * (button_height + button_margin) + button_margin + 100  # 타이틀 공간 추가
                rect = pygame.Rect(x, y, button_width, button_height)
                if bi < len(self.vuSelWordView.vuBtnsWord):
                    self.vuSelWordView.vuBtnsWord[bi].place = rect
                bi += 1  # Increment after use

        def check_answer(button):
            if button.text == self.correct_answer:
                button.color = GREEN
                self.correct_answers += 1
            else:
                button.color = RED
            pygame.time.set_timer(pygame.USEREVENT, 500)


        # 메인 루프
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for aBtn in self.vuSelWordView.vuBtnsWord:
                        if aBtn.is_collide(event.pos):
                            check_answer(aBtn)
                elif event.type == pygame.USEREVENT:
                    self.load_new_question()
                    pygame.time.set_timer(pygame.USEREVENT, 0)
            #self.popup.draw(screen)
            self.vuSelWordView.draw(self.current_page)


            screen.fill(WHITE)
            # 문제 텍스트 그리기
            pygame.draw.rect(screen, self.vuSelWordView.vuBtnWord.color, self.vuSelWordView.vuBtnWord.rect)
            text_surf = font.render(self.vuSelWordView.vuBtnWord.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.vuSelWordView.vuBtnWord.rect.center)
            screen.blit(text_surf, text_rect)

            # 버튼 그리기
            for aBtn in self.vuSelWordView.vuBtnsWord:
                pygame.draw.rect(screen, aBtn.color, aBtn.rect)
                text_surf = font.render(str(aBtn.text), True, BLACK)
                text_rect = text_surf.get_rect(center=aBtn.rect.center)
                screen.blit(text_surf, text_rect)

            #pygame.display.flip()  # 화면 업데이트


    def show_score(self):
        score = (self.correct_answers / 20) * 100  # 점수 계산
        print(f"You got {self.correct_answers} out of 20 correct. Your score: {score}")

if __name__ == "__main__":
    controller = ChoiceController()
    controller.run()
    #controller.show_score_popup(controller.correct_answers) #테스트 종료 후 점수 팝업 표시