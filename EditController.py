import pygame
from pygame.locals import *
from View import View
from Popup import Popup
from Button import Button
from Input import Input
from EditView import EditView
from Search import search
from AddController import AddController


class EditController:
    def __init__(self):
        self.view = View()
        self.editView = EditView()
        self.popup = Popup()

        self.input_box = [Input("단어  ", self.view, self.editView.word_box)]

        self.res = False
        self.word = ""

    def run(self):
        pygame.display.set_caption("단어 수정")
        done = False
        active = 0
        searched = False

        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.editView.search_button.draw(self.view.screen)
            self.input_box[0].draw(self.view.screen)

            if self.res:
                self.editView.edit_button.draw(self.view.screen)
                self.view.draw_text("뜻  ", self.editView.mean_box, 'left_out')
                self.view.draw_text(self.res[0], self.editView.mean_box, 'left_in')
                self.view.draw_text("lv  ", self.editView.lv_box, 'left_out')
                self.view.draw_text(str(self.res[1]), self.editView.lv_box, 'left_in')

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.editView.search_button.is_collide(event.pos):
                        print("검색 버튼 클릭")
                        self.editView.search_button.set_active()
                        self.search_word()
                    if self.res:
                        if self.editView.edit_button.is_collide(event.pos):
                            print("수정 버튼 클릭")
                            AddController("수정", [self.word, self.res[0], self.res[1]]).run()
                            self.res = False
                            self.input_box[0].clear_content()
                            self.word = ""
                            self.popup.hide()

                if event.type == pygame.MOUSEMOTION:
                    self.editView.search_button.is_hover(event.pos)
                    self.editView.edit_button.is_hover(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.input_box[0].handle_input(event)
                    if event.key == pygame.K_RETURN:
                        print("엔터키 입력")
                        self.search_word()

    def search_word(self):
        self.word = self.input_box[0].get_content()
        self.res = search(self.word)
        if self.res:
            print("검색 성공")
            self.popup.show("검색 성공")
        else:
            print("검색 실패")
            self.popup.show("검색 실패")
