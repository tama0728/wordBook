import pygame
import sys
import random
from GameModel import WordModel
from GameView import GameView
from Game.StartScreen import StartScreen
from Game.Pause import Pause
from Game.ShowResult import ShowResult

class GameController:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.model = WordModel(screen_width, screen_height)
        self.view = GameView(screen_width, screen_height)
        self.input_text = ''
        self.clock = pygame.time.Clock()
        self.next_word_time = 0  # 다음 단어 생성까지의 시간
        self.paused = False  # 일시 정지 상태를 나타내는 변수
        self.pause_screen = Pause(pygame.display.set_mode((screen_width, screen_height)), screen_width, screen_height)

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.model.check_input(self.input_text):
                        self.input_text = ''  # 입력한 단어와 같은 단어를 찾으면 입력 텍스트 초기화
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused  # 일시 정지 상태를 토글
                    self.view.toggle_overlay()
                elif event.unicode.isalpha():  # 알파벳만 입력되도록 제한
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
                pos = pygame.mouse.get_pos()
                if self.view.homeButton.is_collide(pos):
                    return False
                if self.view.overlay_visible and self.view.pause.continue_button.collidepoint(pos):
                    self.paused = not self.paused
                    self.view.toggle_overlay()  # 오버레이 해제
                if self.view.overlay_visible and self.view.pause.quit_button.collidepoint(pos):
                    return False
        return True

    '''
    def game_over(self):
        quit_button_rect, restart_button_rect = self.view.display_game_over(self.model.score)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if quit_button_rect.collidepoint(mouse_pos):
                        return False
                    elif restart_button_rect.collidepoint(mouse_pos):
                        self.model.__init__(self.screen_width, self.screen_height)
                        self.input_text = ''
                        return True
    '''

    def run(self, username):
        start_screen = StartScreen(self.view.screen, username)
        gameContinue = start_screen.acid_start()
        show_result = ShowResult(self.view.screen, self.view.screen_width, self.view.screen_height)
        while gameContinue:
            if self.model.lives <= 0:
                gameover = show_result.show_number_result(self.model.score, username)
                #if self.game_over():
                if gameover:
                    self.model.__init__(self.screen_width, self.screen_height)
                    self.input_text = ''
                    continue
                else:
                    break

            TF = self.check_input()
            if(not TF):
                break

            if not self.paused:  # 게임이 일시 정지 상태가 아닐 때만 게임 루프를 실행
                if pygame.time.get_ticks() > self.next_word_time:
                    self.model.generate_word()
                    self.next_word_time = pygame.time.get_ticks() + random.randint(1000, 3000)  # 다음 단어 생성까지의 시간을 랜덤으로 설정

                self.model.update_word_positions()

            self.view.render(self.model.falling_words, self.input_text, self.model.score, self.model.lives)

            if self.paused:
                self.pause_screen.set_overlay_visible(True)
                self.pause_screen.draw()

            self.clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 600
    controller = GameController(screen_width, screen_height)
    controller.run()


'''
import pygame
import sys
import random
from GameModel import WordModel
from GameView import GameView
from Game.StartScreen import StartScreen

class GameController:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.model = WordModel(screen_width, screen_height)
        self.view = GameView(screen_width, screen_height)
        self.input_text = ''
        self.clock = pygame.time.Clock()
        self.next_word_time = 0  # 다음 단어 생성까지의 시간
        self.pause = Pause(pygame.display.set_mode((screen_width, screen_height)), screen_width, screen_height)

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.model.check_input(self.input_text):
                        self.input_text = ''  # 입력한 단어와 같은 단어를 찾으면 입력 텍스트 초기화
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.unicode.isalpha():  # 알파벳만 입력되도록 제한
                    self.input_text += event.unicode

    def game_over(self):
        quit_button_rect, restart_button_rect = self.view.display_game_over(self.model.score)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif restart_button_rect.collidepoint(mouse_pos):
                        self.model.__init__(self.screen_width, self.screen_height)
                        self.input_text = ''
                        return True

    def run(self):
        start_screen = StartScreen(self.view.screen)
        start_screen.acid_start()
        while True:
            if self.model.lives <= 0:
                if self.game_over():
                    continue

            self.check_input()

            if pygame.time.get_ticks() > self.next_word_time:
                self.model.generate_word()
                self.next_word_time = pygame.time.get_ticks() + random.randint(1000, 3000)  # 다음 단어 생성까지의 시간을 랜덤으로 설정

            self.model.update_word_positions()

            self.view.render(self.model.falling_words, self.input_text, self.model.score, self.model.lives)

            self.clock.tick(30)
'''