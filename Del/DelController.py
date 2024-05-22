import pygame

from Del.DelModel import del_word
from Del.DelView import DelView
from View import View
from api.Input import Input
from api.Popup import Popup
from api.Search import search


class DelController:
    def __init__(self):
        self.view = View()
        self.delView = DelView()
        self.popup = Popup()

        self.input_box = [Input("단어  ", self.view, self.delView.word_box)]

        self.res = False

    def run(self):
        pygame.display.set_caption("단어 삭제")
        done = False
        active = 0
        searched = False

        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.delView.search_button.draw(self.view.screen)
            self.input_box[0].draw(self.view.screen)

            if self.res:
                self.delView.del_button.draw(self.view.screen)
                self.view.draw_text("뜻  ", self.delView.mean_box, 'left_out')
                self.view.draw_text(self.res[0], self.delView.mean_box, 'left_in')
                self.view.draw_text("lv  ", self.delView.lv_box, 'left_out')
                self.view.draw_text(str(self.res[1]), self.delView.lv_box, 'left_in')

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.delView.search_button.is_collide(event.pos):
                        print("검색 버튼 클릭")
                        self.delView.search_button.set_active()
                        self.search_word()
                    if self.res:
                        if self.delView.del_button.is_collide(event.pos):
                            print("삭제 버튼 클릭")
                            del_word(self.input_box[0].get_content())
                            self.res = False
                            self.input_box[0].clear_content()
                            self.popup.show("삭제 완료")

                if event.type == pygame.MOUSEMOTION:
                    self.delView.search_button.is_hover(event.pos)
                    self.delView.del_button.is_hover(event.pos)

                if event.type == pygame.KEYDOWN:
                    self.input_box[0].handle_input(event)
                    if event.key == pygame.K_RETURN:
                        print("엔터키 입력")
                        self.search_word()

    def search_word(self):
        word = self.input_box[0].get_content()
        self.res = search(word)
        if self.res:
            print("검색 성공")
            self.popup.show("검색 성공")
        else:
            print("검색 실패")
            self.popup.show("검색 실패")
