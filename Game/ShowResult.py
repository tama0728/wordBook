import pygame
from Game.CheckWriteRanking import CheckWriteRanking

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class ShowResult:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.update_score = CheckWriteRanking()

        pygame.font.init()
        self.font = pygame.font.SysFont("d2coding", 36)

    def show_number_result(self, id, username, number):
        self.update_score.update_user_rain_score(id, number)
        self.update_score.update_rain_ranking(id, username, number)
        result_text = "Result: {}".format(number)
        return self.show_result(result_text)

    def show_time_result(self, elapsed_time, id, username):
        self.update_score.update_user_card_score(id, elapsed_time)
        self.update_score.update_card_ranking(id, username, elapsed_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"종료 시간 : {int(minutes):02d}:{int(seconds):02d}"
        return self.show_result(time_text)

    def show_result(self, result_text):
        text_surface = self.font.render(result_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text_surface, text_rect)

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

        # 사용자의 입력을 기다림
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 마우스 버튼이 눌렸을 때
                    if quit_button_rect.collidepoint(event.pos):
                        return False
                    elif restart_text_rect.collidepoint(event.pos):
                        return True
