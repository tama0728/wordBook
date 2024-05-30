import os

import pygame

from Game.GameRectangle import Rectangle
from Game.Pause import Pause

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class AcidRainView:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1' # 화면을 중앙에 배치
        self.SCREEN_WIDTH = 900
        self.SCREEN_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("d2coding", 32)
        self.input_rect = pygame.Rect(200, 530, 400, 40)
        current_dir = os.path.dirname(__file__)
        self.wave_image_path = os.path.join(current_dir, "assets", "wave.png")
        self.heart_images = [
            pygame.image.load(os.path.join(current_dir,"assets", "pink_heart.png")),
            pygame.image.load(os.path.join(current_dir,"assets", "gray_heart.png"))
        ]
        self.overlay_visible = False
        self.pause = Pause(self.screen)
        self.homeButton = Rectangle(self.SCREEN_WIDTH - 70, self.SCREEN_HEIGHT - 70, 50, 50)
        self.homeButton.set_image(os.path.join(current_dir, 'assets', 'home.png'))


    def toggle_overlay(self):
        self.overlay_visible = not self.overlay_visible

    def draw_text(self, text, x, y, color=BLACK):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_hearts(self, lives):
        for i in range(3):
            heart_image = self.heart_images[0] if i < lives else self.heart_images[1]
            self.screen.blit(heart_image, (20 + i * 40, 20))

    def draw_wave(self):
        image = pygame.image.load(self.wave_image_path)
        image_rect = image.get_rect()
        image_rect.bottom = self.SCREEN_HEIGHT - 70  # 이미지의 아래쪽을 화면 아래에 맞춤
        self.screen.blit(image, image_rect)

    def render(self, falling_words, input_text, score, lives):
        self.screen.fill(WHITE)  # 배경색 채우기
        self.draw_wave()

        # 입력 상자 그리기
        pygame.draw.rect(self.screen, GRAY, self.input_rect)
        self.draw_text(input_text, self.input_rect.x + 5, self.input_rect.y)

        # 단어 그리기
        for word_info in falling_words:
            self.draw_text(word_info["text"], word_info["x"], word_info["y"])

        # 점수 표시
        score_text = self.font.render("Score: {}".format(score), True, BLACK)
        self.screen.blit(score_text, (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

        # 생명 표시
        self.draw_hearts(lives)
        self.homeButton.draw(self.screen)

        if self.overlay_visible:
            self.pause.set_overlay_visible(True)
            self.pause.draw()

        pygame.display.flip()

    def display_game_over(self, score):
        game_over_text = self.font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(game_over_text, game_over_rect)

        # 총 점수 표시
        total_score_text = self.font.render("Total Score: {}".format(score), True, BLACK)
        total_score_rect = total_score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(total_score_text, total_score_rect)

        # 종료 버튼
        quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 50)
        pygame.draw.rect(self.screen, RED, quit_button_rect)
        quit_text = self.font.render("Quit", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        self.screen.blit(quit_text, quit_text_rect)

        # 다시하기 버튼
        restart_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 170, 200, 50)
        pygame.draw.rect(self.screen, GREEN, restart_button_rect)
        restart_text = self.font.render("Restart", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()

        return quit_button_rect, restart_button_rect
