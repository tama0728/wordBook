import pygame
from Button import Button
from Popup import Popup
from UserView import UserView
from View import View
from ShortAnswerTestController import ShortAnswerTestController  # Import the test controller

class UserController:
    def __init__(self, id):
        self.view = View()
        self.userView = UserView(self.view)
        self.popup = Popup()
        self.id = id

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
                        from WordCardController import WordCardController  # 지연 가져오기
                        controller = WordCardController(self.id)
                        controller.run()
                    elif self.userView.test_button.is_collide(event.pos):
                        print("테스트 버튼 클릭")
                        test_controller = ShortAnswerTestController(self.id)  # Instantiate the test controller with user_id
                        test_controller.run()  # Run the test
                    elif self.userView.game_button.is_collide(event.pos):
                        print("게임 버튼 클릭")
                if event.type == pygame.MOUSEMOTION:
                    self.userView.book_button.is_hover(event.pos)
                    self.userView.card_button.is_hover(event.pos)
                    self.userView.test_button.is_hover(event.pos)
                    self.userView.game_button.is_hover(event.pos)

if __name__ == "__main__":
    controller = UserController(id=1)  # Example id
    controller.run()
    pygame.quit()