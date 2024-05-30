import pygame

from Api.Popup import Popup
from Game.AcidRain.AcidRainController import AcidRainController
from Game.CardFlip.CardFlipController import CardFlipController
from Game.GameView import GameView
from View import View


class GameController:
    def __init__(self, user_id, username):
        self.view = View()
        self.gameView = GameView(self.view)
        self.popup = Popup()
        self.user_id = user_id
        self.username = username

    def run(self):
        done = False
        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.gameView.rain_button.draw(self.view.screen)
            self.gameView.card_button.draw(self.view.screen)

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gameView.rain_button.is_collide(event.pos):
                        print("산성비 버튼 클릭")
                        acid_rain_controller = AcidRainController(self.user_id, self.username)
                        acid_rain_controller.run()
                    elif self.gameView.card_button.is_collide(event.pos):
                        print("카드뒤집기 버튼 클릭")
                        card_flip_controller = CardFlipController(self.user_id, self.username)
                        card_flip_controller.run()
                    self.view.set_display_size()
                if event.type == pygame.MOUSEMOTION:
                    self.gameView.rain_button.is_hover(event.pos)
                    self.gameView.card_button.is_hover(event.pos)
