import pygame


class Input:
    def __init__(self, name, view, rect=pygame.Rect(200, 200, 280, 32), limit=17, korean=False):
        self.active = False
        self.name = name
        self.content = ''
        self.view = view
        self.rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.limit = limit
        self.korean = korean

    def draw(self, screen):

        color = self.color_active if self.active else self.color_inactive

        pygame.draw.rect(screen, color, self.rect, 2)
        self.view.draw_text(self.name, self.rect, 'left_out')
        self.view.draw_text(self.content, self.rect, 'left_in')

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.content = self.content[:-1]
        elif len(self.content) >= self.limit:
            pass
        elif 'z' >= event.unicode >= 'a' or 'Z' >= event.unicode >= 'A' or '9' >= event.unicode >= '0':
            self.content += event.unicode
        # elif self.korean:
        #     if 44032 <= ord(event.unicode) <= 55203:
        #         self.content += event.unicode

    def get_content(self):
        return self.content

    def clear_content(self):
        self.content = ''

    def set_content(self, content):
        self.content = content

'''
import pygame
from pygame.locals import *
from ShortAnswerTestModel import ShortAnswerTestModel
from ShortAnswerTestView import ShortAnswerTestView
from hangulInputBox import *


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
        user_answer = self.view.input_box.text + HangulInputBox.engkor(self.view.input_box.hanText)

        # 디버깅을 위한 출력
        print(f"User answer: {user_answer}")

        if self.test_mode == '한->영':
            correct_answer = question.word
        else:
            correct_answer = question.mean

        # 양쪽 공백 제거하고, 소문자로 변환하여 비교
        if user_answer.strip().lower() == correct_answer.strip().lower():
            self.score += 10
            print(f"Correct! Score is now {self.score}")
        else:
            print(user_answer.strip())
            print("Incorrect.")

        self.view.input_box.text = ''
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
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    self.view.input_box.update(event)
                    if event.key == K_RETURN:
                        self.check_answer()
                    self.display_question()
                elif event.type == MOUSEBUTTONDOWN:
                    for level, rect in self.view.level_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_level = level
                            self.display_home()  # 선택된 단계를 반영하기 위해 화면 갱신
                    for mode, rect in self.view.mode_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_mode = mode
                            self.display_home()  # 선택된 모드를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(
                            event.pos) and self.view.selected_level and self.view.selected_mode:
                        self.start_test(self.view.selected_level, self.view.selected_mode)
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
                    for mode, rect in self.view.mode_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.view.selected_mode = mode
                            self.display_home()  # 선택된 모드를 반영하기 위해 화면 갱신
                    if self.view.start_button.collidepoint(
                            event.pos) and self.view.selected_level and self.view.selected_mode:
                        self.start_test(self.view.selected_level, self.view.selected_mode)
        pygame.quit()


if __name__ == "__main__":
    controller = ShortAnswerTestController()
    controller.run()



import pygame
import time
from hangul_utils import join_jamos

class Input:
    cons = {'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
            'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'}
    vowels = {'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ',
              'ho': 'ㅙ', 'hl': 'ㅚ', 'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ'}
    cons_double = {'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ',
                   'fg': 'ㅀ', 'qt': 'ㅄ'}

    def __init__(self, name, view, rect=pygame.Rect(200, 200, 280, 32), limit=17, korean=False):
        self.active = False
        self.name = name
        self.content = ''
        self.view = view
        self.rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.limit = limit
        self.korean = korean
        self.han_text = ''
        self.han_mode = False
        self.font = pygame.font.SysFont(None, 32)
        self.text_image = self.font.render(self.content, True, pygame.Color('black'))
        self.cursor = pygame.Rect(self.text_image.get_rect().topright, (3, self.rect.height - 4))

    def draw(self, screen):
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect, 2)
        self.view.draw_text(self.name, self.rect, 'left_out')
        self.view.draw_text(self.content, self.rect, 'left_in')
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, pygame.Color('black'), self.cursor)

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def handle_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            if self.han_mode and len(self.han_text) > 0:
                self.han_text = self.han_text[:-1]
            elif len(self.content) > 0:
                self.content = self.content[:-1]
        elif len(self.content) >= self.limit:
            return
        elif event.key == pygame.K_RETURN:
            self.content += self.engkor(self.han_text)
            self.han_text = ''
        elif event.key == pygame.K_ESCAPE:
            if self.han_mode:
                self.content += self.engkor(self.han_text)
                self.cursor.width = 3
                self.han_mode = False
            else:
                self.cursor.width = 16
                self.han_mode = True
            self.han_text = ''
        else:
            if self.han_mode:
                self.han_text += event.unicode
            else:
                self.content += event.unicode
        self.update_text_image()

    def update_text_image(self):
        text2 = self.content + self.engkor(self.han_text)
        self.text_image = self.font.render(text2, True, pygame.Color('black'))
        self.cursor.topleft = self.text_image.get_rect().topright

    def get_content(self):
        return self.content

    def clear_content(self):
        self.content = ''
        self.han_text = ''

    def set_content(self, content):
        self.content = content
        self.han_text = ''
        self.update_text_image()

    @classmethod
    def engkor(cls, text):
        result = ''

        vc = ''
        for t in text:
            if t in cls.cons:
                vc += 'c'
            elif t in cls.vowels:
                vc += 'v'
            else:
                vc += '!'

        vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

        i = 0
        while i < len(text):
            v = vc[i]
            t = text[i]

            j = 1
            try:
                if v == 'f' or v == 'c':
                    result += cls.cons[t]
                elif v == 'V':
                    result += cls.vowels[text[i:i + 2]]
                    j += 1
                elif v == 'v':
                    result += cls.vowels[t]
                elif v == 'd':
                    result += cls.cons_double[text[i:i + 2]]
                    j += 1
                else:
                    result += t
            except:
                result += t

            i += j

        return join_jamos(result)
'''