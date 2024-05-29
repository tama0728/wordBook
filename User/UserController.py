import pygame

from User.UserView import UserView
from View import View
from Api.Popup import Popup


class UserController:
    def __init__(self, view, user_id, username):
        self.view = View()
        self.userView = UserView(view)
        self.popup = Popup()
        self.user_id = user_id
        self.username = username

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
                        from BasicWordbook.BasicWordbookController import BasicWordbookController
                        BasicWordbookController = BasicWordbookController(self.user_id)
                        BasicWordbookController.run()
                    elif self.userView.card_button.is_collide(event.pos):
                        print("단어카드 버튼 클릭")
                        from WordCard.WordCardController import WordCardController  # 지연 가져오기
                        WordCardController = WordCardController(self.user_id)
                        WordCardController.run()
                    elif self.userView.test_button.is_collide(event.pos):
                        print("테스트 버튼 클릭")
                        from Test.Short.ShortAnswerTestController import ShortAnswerTestController
                        ShortAnswerTestController = ShortAnswerTestController(self.user_id)
                        ShortAnswerTestController.run()
                    elif self.userView.game_button.is_collide(event.pos):
                        print("게임 버튼 클릭")
                        from Game.GameController import GameController
                        gameHomeController = GameController(self.user_id, self.username)
                        gameHomeController.run()
                    self.view.set_display_size()
                if event.type == pygame.MOUSEMOTION:
                    self.userView.book_button.is_hover(event.pos)
                    self.userView.card_button.is_hover(event.pos)
                    self.userView.test_button.is_hover(event.pos)
                    self.userView.game_button.is_hover(event.pos)

