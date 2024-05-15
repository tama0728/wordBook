import pygame
import AdminModel
from AdminView import AdminView
from Button import Button
from Popup import Popup


class AdminController:
    def __init__(self):
        # self.model = AdminHomeModel()
        self.view = AdminView()
        self.popup = Popup()
        # self.controller = AdminHomeController(self.model, self.view)

    def run(self):
        clock = pygame.time.Clock()
        self.popup.show("로그인 성공")
        add_button = Button(100, 100, 100, 50, "추가")
        del_button = Button(100, 200, 100, 50, "삭제")
        edit_button = Button(100, 300, 100, 50, "수정")

        self.view.screen.fill((255, 255, 255))

        add_button.draw(self.view.screen)
        del_button.draw(self.view.screen)
        edit_button.draw(self.view.screen)

        self.popup.draw(self.view.screen)
        pygame.display.flip()
        clock.tick(30)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.is_clicked(event.pos):
                        print("추가 버튼 클릭")
                    elif del_button.is_clicked(event.pos):
                        print("삭제 버튼 클릭")
                    elif edit_button.is_clicked(event.pos):
                        print("수정 버튼 클릭")

