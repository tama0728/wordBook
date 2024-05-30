import pygame

from Api.Button import Button
from View import View


class GameView:
    def __init__(self, view: View):

        self.boxWidth, self.boxHeight = 150, 75
        self.boxLeft = (view.WIDTH - self.boxWidth) // 2
        self.boxTop = (view.HEIGHT - self.boxHeight) // 2
        self.rain_button = Button(pygame.Rect(self.boxLeft - 100, self.boxTop, self.boxWidth, self.boxHeight), "산성비")
        self.card_button = Button(pygame.Rect(self.boxLeft + 100, self.boxTop, self.boxWidth, self.boxHeight), "카드뒤집기")
