import pygame
import sys
import os
from Game.GameRectangle import Rectangle
from Game.ShowRanking import ShowRanking

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


# StartScreen 클래스
class StartScreen:
    def __init__(self, screen, user_id, username):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.game_name = Rectangle(20, 20, 200, 50, GRAY)
        self.start_button = Rectangle(self.screen_width - 200, self.screen_height - 150, 150, 50, GRAY)
        self.home_button = Rectangle(self.screen_width - 70, self.screen_height - 70, 50, 50)
        current_dir = os.path.dirname(__file__)
        self.home_button.set_image(os.path.join(current_dir, 'CardFlip', 'assets', 'home.png'))
        self.user_id = user_id
        self.username = username
        self.Ranking = ShowRanking(screen)

    def acid_start(self):
        self.game_name.set_text("산성비")
        self.screen.fill(WHITE)
        self.Ranking.draw_rain_ranking(self.user_id, self.username)
        return self.run()

    def card_start(self):
        self.game_name.set_text("카드 뒤집기")
        self.screen.fill(WHITE)
        self.Ranking.draw_card_ranking(self.user_id, self.username)
        return self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return True
                    elif self.home_button.collidepoint(event.pos):
                        return False

            # 게임 이름 텍스트
            self.start_button.set_text("시작하기")
            self.start_button.draw(self.screen)

            # 홈 버튼
            self.home_button.draw(self.screen)

            self.game_name.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)
