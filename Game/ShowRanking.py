import pygame
from Game.CheckWriteRanking import CheckWriteRanking


class ShowRanking:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.check_Ranking = CheckWriteRanking()

    def draw_rain_ranking(self, user_id, username):
        ranking_rain = self.check_Ranking.get_current_rain_ranking()
        user_scores = self.check_Ranking.get_user_scores(user_id)
        font = pygame.font.SysFont("d2coding", 36)
        text_height = font.size("Test")[1]  # 텍스트의 높이를 가져옵니다.
        total_text_height = len(ranking_rain) * (text_height + 10)  # 모든 텍스트의 총 높이를 계산합니다.
        start_y = (self.screen_height - total_text_height) // 2  # 시작 y 위치를 계산합니다.
        background_color = (192, 192, 192)  # 회색
        text_color = (0, 0, 0)  # 검정색
        padding = 10  # 사각형 내부 여백
        border_radius = 10  # 둥근 모서리

        # "RANKING" 텍스트 그리기
        ranking_text = font.render("RANKING", True, text_color)
        ranking_text_rect = ranking_text.get_rect(midtop=(self.screen_width // 2, start_y - 50))
        # 배경 사각형 그리기
        pygame.draw.rect(self.screen, background_color, ranking_text_rect.inflate(padding * 2, padding * 2),
                         border_radius=border_radius)
        self.screen.blit(ranking_text, ranking_text_rect)

        for index, entry in enumerate(ranking_rain):
            username = entry[0]
            score = entry[1]
            text = font.render(f"{index + 1}. {username:20} {score}", True, text_color)
            text_rect = text.get_rect(midtop=(self.screen_width // 2, start_y + index * (text_height + 10)))
            # 배경 사각형 그리기
            pygame.draw.rect(self.screen, background_color, text_rect.inflate(padding * 2, padding * 2),
                             border_radius=border_radius)
            self.screen.blit(text, text_rect)

        # 사용자 최고 점수 그리기
        user_high_scores_text = f"{user_scores[0]}'s best Scores : {user_scores[2]}"
        user_high_scores_surface = font.render(user_high_scores_text, True, text_color)
        user_high_scores_rect = user_high_scores_surface.get_rect(
            midtop=(self.screen_width // 2, start_y + len(ranking_rain) * (text_height + 10) + 50))
        # 배경 사각형 그리기
        pygame.draw.rect(self.screen, background_color, user_high_scores_rect.inflate(padding * 2, padding * 2),
                         border_radius=border_radius)
        self.screen.blit(user_high_scores_surface, user_high_scores_rect)

    def draw_card_ranking(self, user_id, username):
        ranking_card = self.check_Ranking.get_current_card_ranking()
        user_scores = self.check_Ranking.get_user_scores(user_id)
        font = pygame.font.SysFont("d2coding", 36)
        text_height = font.size("Test")[1]  # 텍스트의 높이를 가져옵니다.
        total_text_height = len(ranking_card) * (text_height + 10)  # 모든 텍스트의 총 높이를 계산합니다.
        start_y = (self.screen_height - total_text_height) // 2  # 시작 y 위치를 계산합니다.
        background_color = (192, 192, 192)  # 회색
        text_color = (0, 0, 0)  # 검정색
        padding = 10  # 사각형 내부 여백
        border_radius = 10  # 둥근 모서리

        # "RANKING" 텍스트 그리기
        ranking_text = font.render("RANKING", True, text_color)
        ranking_text_rect = ranking_text.get_rect(midtop=(self.screen_width // 2, start_y - 50))
        # 배경 사각형 그리기
        pygame.draw.rect(self.screen, background_color, ranking_text_rect.inflate(padding * 2, padding * 2),
                         border_radius=border_radius)
        self.screen.blit(ranking_text, ranking_text_rect)

        for index, entry in enumerate(ranking_card):
            username = entry[0]
            score = entry[1]
            minutes = score // 60
            seconds = score % 60
            text = font.render(f"{index + 1}. {username:20} {minutes:02d}:{seconds:02d}", True, text_color)
            text_rect = text.get_rect(midtop=(self.screen_width // 2, start_y + index * (text_height + 10)))
            # 배경 사각형 그리기
            pygame.draw.rect(self.screen, background_color, text_rect.inflate(padding * 2, padding * 2),
                             border_radius=border_radius)
            self.screen.blit(text, text_rect)

        # 사용자 최고 점수 그리기
        user_high_scores_text = f"{user_scores[0]}'s best Scores : {user_scores[1]}"
        user_high_scores_surface = font.render(user_high_scores_text, True, text_color)
        user_high_scores_rect = user_high_scores_surface.get_rect(
            midtop=(self.screen_width // 2, start_y + len(ranking_card) * (text_height + 10) + 50))
        # 배경 사각형 그리기
        pygame.draw.rect(self.screen, background_color, user_high_scores_rect.inflate(padding * 2, padding * 2),
                         border_radius=border_radius)
        self.screen.blit(user_high_scores_surface, user_high_scores_rect)
