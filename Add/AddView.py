import pygame

from Api.Button import Button


class AddView:
    def __init__(self, text="추가"):
        self.add_button = Button(pygame.Rect(200, 370, 130, 50), text)
        self.cancel_button = Button(pygame.Rect(350, 370, 130, 50), "취소")

        self.word_box = pygame.Rect(200, 100, 300, 50)
        self.mean_box = pygame.Rect(200, 200, 300, 50)
        self.sentence_box = pygame.Rect(200, 300, 300, 50)
        self.lv_box = pygame.Rect(200, 300, 300, 50)

        self.checkBox = pygame.Rect(255, 310, 30, 30)
