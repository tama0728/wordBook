import pygame

from api.Button import Button


class DelView:
    def __init__(self):
        self.search_button = Button(pygame.Rect(200, 370, 130, 50), "찾기")
        self.del_button = Button(pygame.Rect(350, 370, 130, 50), "삭제")

        self.word_box = pygame.Rect(200, 100, 300, 50)

        self.mean_box = pygame.Rect(200, 200, 300, 50)
        self.sentence_box = pygame.Rect(200, 300, 300, 50)
        self.lv_box = pygame.Rect(200, 300, 300, 50)

        # self.checkBox = pygame.Rect(255, 310, 30, 30)
