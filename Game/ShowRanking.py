import pygame
from Game.Check_Write_Ranking  import Check_Write_Ranking

class ShowRanking:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.check_Ranking = Check_Write_Ranking()

    def get_card_ranking(self):
        # 상위 3명의 순위 가져오기
        return self.check_Ranking.get_current_card_ranking()

    def get_rain_ranking(self):
        # 상위 3명의 순위 가져오기
        return self.check_Ranking.get_current_rain_ranking()

    def draw_rain_ranking(self):
        ranking = self.get_rain_ranking()
        font = pygame.font.SysFont(None, 36)
        text_y = 100
        for index, entry in enumerate(ranking):
            username = entry['username']
            score = entry['score']
            text = font.render(f"{index + 1}. {username}: {score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, text_y))
            self.screen.blit(text, text_rect)
            text_y += 50

    def draw_card_ranking(self):
        ranking = self.get_card_ranking()
        font = pygame.font.SysFont(None, 36)
        text_y = 100
        for index, entry in enumerate(ranking):
            username = entry['username']
            score = entry['score']
            text = font.render(f"{index + 1}. {username}: {score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, text_y))
            self.screen.blit(text, text_rect)
            text_y += 50
