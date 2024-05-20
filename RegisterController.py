import pygame
from pygame.locals import *
from RegisterModel import RegisterModel
from RegisterView import RegisterView
from Popup import Popup
from View import View
from Input import Input
from hashlib import sha256


class RegisterController:
    def __init__(self):
        self.done = None
        self.model = RegisterModel()
        self.view = View()
        self.registerView = RegisterView(self.view)
        self.popup = Popup()
        self.registered = False

    def run(self):
        pygame.display.set_caption("회원가입")
        self.registered = False
        self.done = False
        clock = pygame.time.Clock()
        active = 0

        input_box = [Input("ID:", self.view, self.registerView.id_box),
                     Input("Password:", self.view, self.registerView.password_box),
                     Input("Phone:", self.view, self.registerView.phone_box)]

        while not self.done:
            self.view.screen.fill((255, 255, 255))

            for i in range(len(input_box)):
                if i == active:
                    input_box[i].set_active()
                else:
                    input_box[i].set_inactive()
                input_box[i].draw(self.view.screen)

            self.registerView.register_button.draw(self.view.screen)

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                if event.type == KEYDOWN:
                    input_box[active].handle_input(event)
                    if event.key == K_TAB:
                        active += 1
                        active %= len(input_box)
                    elif event.key == K_RETURN:
                        self.register(input_box[0].get_content(),
                                      sha256(input_box[1].get_content().encode('utf-8')).hexdigest(),
                                      input_box[2].get_content())

                if event.type == MOUSEBUTTONDOWN:
                    if self.registerView.id_box.collidepoint(event.pos):
                        active = 0
                    elif self.registerView.password_box.collidepoint(event.pos):
                        active = 1
                    elif self.registerView.phone_box.collidepoint(event.pos):
                        active = 2
                    elif self.registerView.register_button.is_collide(event.pos):
                        self.register(input_box[0].get_content(),
                                      sha256(input_box[1].get_content().encode('utf-8')).hexdigest(),
                                      input_box[2].get_content())

        return self.registered

    def register(self, username, password, phone):
        if self.model.register(username, password, phone):
            print("회원가입 성공")
            self.registered = True
            self.done = True
        else:
            print("회원가입 실패")
            self.popup.show("회원가입 실패")
