import pygame

from Popup import Popup
from UserView import UserView
from View import View


class UserController:
    def __init__(self):
        self.view = View()
        self.userView = UserView(self.view)
        self.popup = Popup()

    def run(self):
        done = False
        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.userView.book_button.draw(self.view.screen)
            self.userView.card_button.draw(self.view.screen)
            self.userView.test_button.draw(self.view.screen)
            self.userView.game_button.draw(self.view.screen)

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.userView.book_button.is_collide(event.pos):
                        print("단어장 버튼 클릭")
                    elif self.userView.card_button.is_collide(event.pos):
                        print("단어카드 버튼 클릭")
                    elif self.userView.test_button.is_collide(event.pos):
                        print("테스트 버튼 클릭")
                    elif self.userView.game_button.is_collide(event.pos):
                        print("게임 버튼 클릭")
                if event.type == pygame.MOUSEMOTION:
                    self.userView.book_button.is_hover(event.pos)
                    self.userView.card_button.is_hover(event.pos)
                    self.userView.test_button.is_hover(event.pos)
                    self.userView.game_button.is_hover(event.pos)

