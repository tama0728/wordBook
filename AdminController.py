import pygame

from AddController import AddController
from AdminView import AdminView
from DelController import DelController
from EditController import EditController
from Popup import Popup
from View import View

class AdminController:
    def __init__(self, user_id):  # user_id를 인자로 받음
        self.view = View()
        self.adminView = AdminView(self.view)
        self.popup = Popup()
        self.user_id = user_id  # user_id 저장

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