import pygame
from hangulInputBox import HangulInputBox

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
        self.start_button = pygame.Rect(300, 250, 200, 50)
        self.input_box = HangulInputBox('NanumBarunGothic.ttf', 32, 400 // 16, 'black', 'gray')
        self.input_box.rect.center = (400, 500)

        self.selected_level = None

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

        pygame.draw.rect(self.screen, (0, 0, 0), self.start_button, 2)
        start_surface = self.font_small.render("Start", True, (0, 0, 0))
        self.screen.blit(start_surface, (self.start_button.x + 60, self.start_button.y + 10))
        pygame.display.flip()

    def display_question(self, question, user_input):
        self.screen.fill((255, 255, 255))
        question_surface = self.font.render(question, True, (0, 0, 0))
        self.screen.blit(question_surface, (400 - question_surface.get_width() // 2, 200))

        # Draw light blue rectangle
        pygame.draw.rect(self.screen, (173, 216, 230), (100, 400, 600, 50))  # Light blue rectangle
        self.input_box.text = user_input
        self.input_box.draw(self.screen)

        pygame.display.flip()

    def display_result(self, score):
        self.screen.fill((255, 255, 255))
        result_surface = self.font.render(f"Your Score: {score}", True, (0, 0, 0))
        self.screen.blit(result_surface, (400 - result_surface.get_width() // 2, 200))
        pygame.display.flip()