from hashlib import sha256

import pygame
from pygame.locals import *

from Admin.AdminController import AdminController
from Login.LoginModel import LoginModel
from Login.LoginView import LoginView
from Register.RegisterController import RegisterController
from User.UserController import UserController
from View import View
from Api.Input import Input
from Api.Popup import Popup


class Controller:
    def __init__(self):
        pygame.init()
        self.loginModel = LoginModel()
        self.view = View()
        self.loginView = LoginView(self.view)
        self.popup = Popup()
        self.register_controller = RegisterController()
        self.done = False

    def run(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption("로그인")
        active = 0
        id_box = self.loginView.id_box
        password_box = self.loginView.password_box
        input_box = [Input("ID:", self.view, id_box),
                     Input("Password:", self.view, password_box)]

        while not self.done:
            self.view.screen.fill((255, 255, 255))
            self.loginView.login_button.draw(self.view.screen)
            self.loginView.register_button.draw(self.view.screen)

            for i in range(len(input_box)):
                if i == active:
                    input_box[i].set_active()
                else:
                    input_box[i].set_inactive()
                input_box[i].draw(self.view.screen)

            self.popup.draw(self.view.screen)  # 팝업 메시지 그리기

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True

                if event.type == KEYDOWN:
                    input_box[active].handle_input(event)
                    if event.key == K_TAB:
                        active += 1
                        active %= 2
                    elif event.key == K_RETURN:
                            self.login(input_box[0].get_content(), sha256(input_box[1].get_content().encode('utf-8')).hexdigest())
                            input_box[0].clear_content()
                            input_box[1].clear_content()

                if event.type == MOUSEBUTTONDOWN:
                    if id_box.collidepoint(event.pos):
                        active = 0
                    elif password_box.collidepoint(event.pos):
                        active = 1

                    elif self.loginView.login_button.is_collide(event.pos):  # 로그인 버튼 클릭 처리
                        self.login(input_box[0].get_content(),
                                   sha256(input_box[1].get_content().encode('utf-8')).hexdigest())
                        input_box[0].clear_content()
                        input_box[1].clear_content()

                    elif self.loginView.register_button.is_collide(event.pos):  # 회원가입 버튼 클릭 처리
                        self.popup.hide()
                        self.register_controller.run()
                        if self.register_controller.registered:
                            print("회원가입 성공")
                            self.popup.show("회원가입 성공")
                        pygame.display.set_caption("로그인")
                        active = 0

                if event.type == MOUSEMOTION:
                    self.loginView.login_button.is_hover(event.pos)
                    self.loginView.register_button.is_hover(event.pos)

    def login(self, username, password):
        username = username.strip()
        password = password.strip()
        if len(username) < 3 or len(password) < 3:
            print("아이디 또는 비밀번호는 3글자 이상이어야 합니다.")
            self.popup.show("아이디 또는 비밀번호는 3글자 이상이어야 합니다.")
            return
        id = self.loginModel.login(username, password)
        if id:
            print("로그인 성공")
            # self.done = True
            res = self.loginModel.get_admin(id)
            if self.loginModel.get_admin(id):
                print("관리자 로그인")
                admin = AdminController()
                admin.run()
            else:
                print("사용자 로그인")
                user = UserController(self.view, id, username)
                user.run()
        else:
            print("로그인 실패")
            self.popup.show("로그인 실패")

    def __del__(self):
        pygame.quit()
