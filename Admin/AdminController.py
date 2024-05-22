import pygame

from Add.AddController import AddController
from Admin.AdminView import AdminView
from Del.DelController import DelController
from Edit.EditController import EditController
from View import View
from Api.Popup import Popup


class AdminController:
    def __init__(self):
        self.view = View()
        self.adminView = AdminView(self.view)
        self.popup = Popup()

    def run(self):
        pygame.display.set_caption("관리자")
        done = False
        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.adminView.add_button.draw(self.view.screen)
            self.adminView.del_button.draw(self.view.screen)
            self.adminView.edit_button.draw(self.view.screen)

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.adminView.add_button.is_collide(event.pos):
                        print("추가 버튼 클릭")
                        addController = AddController()
                        addController.run()

                    elif self.adminView.del_button.is_collide(event.pos):
                        print("삭제 버튼 클릭")
                        delController = DelController()
                        delController.run()
                    elif self.adminView.edit_button.is_collide(event.pos):
                        print("수정 버튼 클릭")
                        editController = EditController()
                        editController.run()
                if event.type == pygame.MOUSEMOTION:
                    self.adminView.add_button.is_hover(event.pos)
                    self.adminView.del_button.is_hover(event.pos)
                    self.adminView.edit_button.is_hover(event.pos)

            pygame.display.set_caption("관리자")
