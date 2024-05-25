import pygame
from hangulInputBox import *

class ShortAnswerTestView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Malgun Gothic", 48)
        self.font_small = pygame.font.SysFont("Malgun Gothic", 28)
        self.font_tiny = pygame.font.SysFont("Malgun Gothic", 18)

        self.level_buttons = {
            '1': pygame.Rect(100, 150, 100, 50),
            '2': pygame.Rect(250, 150, 100, 50),
            '3': pygame.Rect(400, 150, 100, 50),
        }
        self.mode_buttons = {
            '한->영': pygame.Rect(100, 350, 150, 50),
            '영->한': pygame.Rect(300, 350, 150, 50),
        }
        self.start_button = pygame.Rect(300, 450, 200, 50)
        self.input_box = HangulInputBox('NanumBarunGothic.ttf', 32, 20, 'black', 'gray')
        self.input_box.rect.center = (400, 400)  # 화면 중앙에 위치

        self.selected_level = None
        self.selected_mode = None

    def draw_text(self, text, rect, position):
        if position == 'left_out':
            pos = (rect.x - rect.width // 2 + 10, rect.y + rect.height // 2 - 10)
        else:  # 'left_in'
            pos = (rect.x + 10, rect.y + rect.height // 2 - 10)
        text_surface = self.font_small.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, pos)

    def display_home(self):
        self.screen.fill((255, 255, 255))
        for level, rect in self.level_buttons.items():
            color = (0, 255, 0) if self.selected_level == level else (0, 0, 0)
            pygame.draw.rect(self.screen, color, rect, 2)
            label_surface = self.font_small.render(f"Level {level}", True, color)
            self.screen.blit(label_surface, (rect.x + 10, rect.y + 10))

        for mode, rect in self.mode_buttons.items():
            color = (0, 255, 0) if self.selected_mode == mode else (0, 0, 0)
            pygame.draw.rect(self.screen, color, rect, 2)
            mode_surface = self.font_small.render(mode, True, color)
            self.screen.blit(mode_surface, (rect.x + 10, rect.y + 10))

        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 2)
        start_surface = self.font_small.render("Start", True, (0, 0, 0))
        self.screen.blit(start_surface, (self.start_button.x + 60, self.start_button.y + 10))
        pygame.display.flip()

    def display_question(self, question, user_input):
        self.screen.fill((255, 255, 255))
        question_surface = self.font.render(question, True, (0, 0, 0))
        self.screen.blit(question_surface, (400 - question_surface.get_width() // 2, 200))
        self.input_box.update(None)
        self.input_box.image.fill(self.input_box.bColor)
        self.input_box.image.blit(self.input_box.textImage, self.input_box.textRect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(self.input_box.image, 'black', self.input_box.cursor)
        self.screen.blit(self.input_box.image, self.input_box.rect)
        pygame.display.flip()

    def display_result(self, score):
        self.screen.fill((255, 255, 255))
        result_surface = self.font.render(f"Your Score: {score}", True, (0, 0, 0))
        self.screen.blit(result_surface, (400 - result_surface.get_width() // 2, 200))
        pygame.display.flip()