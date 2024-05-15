import pygame
from pygame.locals import *
from LoginModel import LoginModel
from LoginView import LoginView
from RegisterController import RegisterController
from Popup import Popup
from AdminController import AdminController


class Controller:
    def __init__(self):
        self.loginModel = LoginModel()
        self.loginView = LoginView()
        self.popup = Popup()
        self.register_controller = RegisterController()

    def run(self):
        clock = pygame.time.Clock()
        username = ''
        password = ''
        input_box1 = pygame.Rect(200, 200, 280, 32)
        input_box2 = pygame.Rect(200, 250, 280, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = 0

        login_button = pygame.Rect(200, 320, 130, 50)
        register_button = pygame.Rect(350, 320, 130, 50)

        done = False
        while not done:
            self.loginView.screen.fill((255, 255, 255))

            color1 = color_active if active == 0 else color_inactive
            color2 = color_active if active == 1 else color_inactive

            pygame.draw.rect(self.loginView.screen, color1, input_box1, 2)
            pygame.draw.rect(self.loginView.screen, color2, input_box2, 2)
            pygame.draw.rect(self.loginView.screen, color_inactive, login_button, 2)
            pygame.draw.rect(self.loginView.screen, (0, 255, 0), register_button)

            self.loginView.draw_text('ID:', input_box1, 'left_out')
            self.loginView.draw_text('Password:', input_box2, 'left_out')
            self.loginView.draw_text('Login', login_button)
            self.loginView.draw_text('Register', register_button)

            self.loginView.draw_text(username, input_box1, 'left_in')
            self.loginView.draw_text(password, input_box2, 'left_in')

            self.popup.draw(self.loginView.screen)  # 팝업 메시지 그리기

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_TAB:
                        active += 1
                        active %= 2
                    elif active is not None:
                        if event.key == K_BACKSPACE:
                            if active == 0:
                                username = username[:-1]
                            elif active == 1:
                                password = password[:-1]
                        elif event.key == K_RETURN:
                            if self.loginModel.login(username, password):
                                self.loginModel = LoginModel()
                                print("로그인 성공")
                                done = True
                                admin = AdminController()
                                admin.run()
                            else:
                                print("로그인 실패")
                                self.popup.show("로그인 실패")
                            username = ''
                            password = ''
                        else:
                            if active == 0:
                                username += event.unicode
                            elif active == 1:
                                password += event.unicode

                if event.type == MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active = 0
                    elif input_box2.collidepoint(event.pos):
                        active = 1
                    elif login_button.collidepoint(event.pos):
                        if self.loginModel.login(username, password):
                            print("로그인 성공")
                            self.popup.show("로그인 성공")
                            done = True
                            admin = AdminController()
                            admin.run()
                        else:
                            print("로그인 실패")
                            self.popup.show("로그인 실패")
                        username = ''
                        password = ''
                    elif register_button.collidepoint(event.pos):  # 회원가입 버튼 클릭 처리
                        self.popup.hide()
                        self.register_controller.run()
                        if self.register_controller.registered:
                            print("회원가입 성공")
                            self.popup.show("회원가입 성공")
                        pygame.display.set_caption("로그인")
                        active = 0
                        self.loginView.screen.fill((255, 255, 255))  # 다시 로그인 화면으로 돌아올 때 화면 초기화

