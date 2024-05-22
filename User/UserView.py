import pygame

from View import View
from api.Button import Button


class UserView:
    def __init__(self, view: View):
        self.boxWidth, self.boxHeight = 150, 75
        self.boxLeft = (view.WIDTH - self.boxWidth) // 2
        self.boxTop = (view.HEIGHT - self.boxHeight) // 2
        self.book_button = Button(pygame.Rect(self.boxLeft - 100, self.boxTop - 50, self.boxWidth, self.boxHeight), "단어장")
        self.card_button = Button(pygame.Rect(self.boxLeft - 100, self.boxTop + 50, self.boxWidth, self.boxHeight), "단어카드")
        self.test_button = Button(pygame.Rect(self.boxLeft + 100, self.boxTop - 50, self.boxWidth, self.boxHeight), "테스트")
        self.game_button = Button(pygame.Rect(self.boxLeft + 100, self.boxTop + 50, self.boxWidth, self.boxHeight), "게임")
