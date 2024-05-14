import pygame
import AdminModel
import AdminHomeView
import AdminController

class AdminHome:
    def __init__(self):
        # self.model = AdminHomeModel()
        self.view = AdminHomeView
        # self.controller = AdminHomeController(self.model, self.view)

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.collidepoint(event.pos):
                        print("추가 버튼 클릭")
                    elif del_button.collidepoint(event.pos):
                        print("삭제 버튼 클릭")
                    elif edit_button.collidepoint(event.pos):
                        print("수정 버튼 클릭")
            pygame.display.flip()