import random
import sys

import pygame

from Game.AcidRain.AcidRainModel import AcidRainModel
from Game.AcidRain.AcidRainView import AcidRainView
from Game.Pause import Pause
from Game.ShowResult import ShowResult
from Game.StartScreen import StartScreen


class AcidRainController:
    def __init__(self, user_id, username):
        self.model = AcidRainModel()
        self.acidRainView = AcidRainView()
        self.input_text = ''
        self.clock = pygame.time.Clock()
        self.next_word_time = 0  # 다음 단어 생성까지의 시간
        self.paused = False  # 일시 정지 상태를 나타내는 변수
        self.screen = pygame.display.set_mode((self.acidRainView.SCREEN_WIDTH, self.acidRainView.SCREEN_HEIGHT))
        self.pause_screen = Pause(self.screen)
        self.id = user_id
        self.username = username

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.model.check_input(self.input_text)
                    self.input_text = ''  # 입력한 단어와 같은 단어를 찾으면 입력 텍스트 초기화
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused  # 일시 정지 상태를 토글
                    self.acidRainView.toggle_overlay()
                elif event.unicode.isalpha():  # 알파벳만 입력되도록 제한
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트 처리
                pos = pygame.mouse.get_pos()
                if self.acidRainView.homeButton.is_collide(pos):
                    return False
                if self.acidRainView.overlay_visible and self.acidRainView.pause.continue_button.collidepoint(pos):
                    self.paused = not self.paused
                    self.acidRainView.toggle_overlay()  # 오버레이 해제
                if self.acidRainView.overlay_visible and self.acidRainView.pause.quit_button.collidepoint(pos):
                    return False
        return True

    def run(self):
        start_screen = StartScreen(self.screen, self.id, self.username)
        gameContinue = start_screen.acid_start()
        show_result = ShowResult(self.screen)
        while gameContinue:
            if self.model.lives <= 0:
                gameover = show_result.show_number_result(self.id, self.username, self.model.score)
                if gameover:
                    self.model.__init__()
                    self.input_text = ''
                    continue
                else:
                    break

            TF = self.check_input()
            if (not TF):
                break

            if not self.paused:  # 게임이 일시 정지 상태가 아닐 때만 게임 루프를 실행
                if pygame.time.get_ticks() > self.next_word_time:
                    self.model.generate_word()
                    self.next_word_time = pygame.time.get_ticks() + random.randint(1000,3000)  # 다음 단어 생성까지의 시간을 랜덤으로 설정

                self.model.update_word_positions()

            self.acidRainView.render(self.model.falling_words, self.input_text, self.model.score, self.model.lives)

            if self.paused:
                self.pause_screen.set_overlay_visible(True)
                self.pause_screen.draw()

            self.clock.tick(30)
