import pygame

from Add.AddModel import add_word
from Add.AddView import AddView
from Edit.EditModel import edit_word
from View import View
from Api.CheckBox import CheckBox
from Api.Input import Input
from Api.Popup import Popup
from Api.hangulInputBox import HangulInputBox as hangulInputBox



class AddController:
    def __init__(self, text="추가", res=None):
        self.view = View()
        self.addView = AddView(text)
        self.popup = Popup()
        self.res = res

        self.input_box = Input("단어  ", self.view, self.addView.word_box)
        self.meanBox = hangulInputBox("d2coding", 32, 14, 'black', 'gray')
        self.meanBox.rect.center = self.addView.mean_box.center

        self.checkBoxs = [CheckBox("Lv.1 ", self.view, self.addView.checkBox),
                         CheckBox("Lv.2 ", self.view, self.addView.checkBox.move(100, 0)),
                         CheckBox("Lv.3 ", self.view, self.addView.checkBox.move(200, 0))
                         ]
        self.lv = 0

    def run(self):
        if self.res is None:
            pygame.display.set_caption("단어 추가")
        else:
            pygame.display.set_caption("단어 수정")
            self.input_box.set_content(self.res[0])
            self.meanBox.set_content(self.res[1])
            self.lv = self.res[2]
            self.checkBoxs[self.lv - 1].check()

        done = False
        active = 0

        while not done:
            clock = pygame.time.Clock()

            self.view.screen.fill((255, 255, 255))

            self.addView.add_button.draw(self.view.screen)
            self.addView.cancel_button.draw(self.view.screen)
            self.view.draw_text("lv  ", self.addView.lv_box, 'left_out')

            for i in range(len(self.checkBoxs)):
                self.checkBoxs[i].draw()

            if 0 == active:
                self.input_box.set_active()
            # else:
            #     self.meanBox.update(None)
            self.input_box.draw(self.view.screen)
            self.meanBox.draw(self.view.screen)

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.checkBoxs)):
                        if self.checkBoxs[i].is_collide(event.pos):
                            self.lv = i + 1

                    for j in range(len(self.checkBoxs)):
                        if j == self.lv - 1:
                            self.checkBoxs[j].check()
                        else:
                            self.checkBoxs[j].uncheck()

                    if self.addView.add_button.is_collide(event.pos):
                        if self.res is not None:
                            done = self.edit_word(self.res[0])
                        else:
                            done = self.add_word()

                    elif self.addView.cancel_button.is_collide(event.pos):
                        print("취소 버튼 클릭")
                        done = True
                    elif self.addView.word_box.collidepoint(event.pos):
                        active = 0
                    elif self.addView.mean_box.collidepoint(event.pos):
                        active = 1
                if event.type == pygame.MOUSEMOTION:
                    self.addView.add_button.is_hover(event.pos)
                    self.addView.cancel_button.is_hover(event.pos)

                if event.type == pygame.KEYDOWN:
                    if active == 0:
                        self.input_box.handle_input(event)
                    elif active == 1:
                        self.meanBox.update(event)
                    if event.key == pygame.K_TAB:
                        active = (active + 1) % 2
                    if event.key == pygame.K_RETURN:
                        if active == 1:
                            if self.res is not None:
                                done = self.edit_word(self.res[0])
                            else:
                                done = self.add_word()

    def add_word(self):
        print("추가 버튼 클릭")
        word = self.input_box.get_content()
        mean = self.meanBox.get_content()
        # sentence = self.input_box[2].get_content()
        lv = self.lv

        if add_word(word, mean, lv):
            print("단어 추가 성공")
            return True
        else:
            print("단어 추가 실패")
            self.popup.show("단어 추가 실패")

    def edit_word(self, original_word):
        print("수정 버튼 클릭")
        word = self.input_box.get_content()
        mean = self.meanBox.get_content()
        lv = self.lv

        if edit_word(original_word, word, mean, lv):
            print("단어 수정 성공")
            return True
        else:
            print("단어 수정 실패")
            self.popup.show("단어 수정 실패")
