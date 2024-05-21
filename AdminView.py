import pygame

from Button import Button
from View import View


class AdminView:
    def __init__(self, view: View):
        self.boxWidth = 100
        self.boxLeft = (view.WIDTH - self.boxWidth) // 2
        self.add_button = Button(pygame.Rect(self.boxLeft, 100, self.boxWidth, 50), "추가")
        self.del_button = Button(pygame.Rect(self.boxLeft, 200, self.boxWidth, 50), "삭제")
        self.edit_button = Button(pygame.Rect(self.boxLeft, 300, self.boxWidth, 50), "수정")
