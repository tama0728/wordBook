import pygame
from pygame.locals import *
from RegisterModel import RegisterModel
from RegisterView import RegisterView
from Popup import Popup


class RegisterController:
    def __init__(self):
        self.model = RegisterModel()
        self.registered = None
        self.view = RegisterView()
        self.popup = Popup()

    def run(self):
        pygame.display.set_caption("회원가입")
        self.registered = False
        self.model = RegisterModel()
        clock = pygame.time.Clock()
        username = ''
        password = ''
        input_box1 = pygame.Rect(200, 200, 280, 32)
        input_box2 = pygame.Rect(200, 250, 280, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = 0

        register_button = pygame.Rect(200, 320, 280, 50)

        done = False
        while not done:
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
                            if self.model.register(username, password):
                                print("회원가입 성공")
                                self.registered = True
                                done = True
                            else:
                                print("회원가입 실패")
                                self.popup.show("회원가입 실패")
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
                    elif register_button.collidepoint(event.pos):
                        if self.model.register(username, password):
                            print("회원가입 성공")
                            self.registered = True
                            done = True
                        else:
                            print("회원가입 실패")
                            self.popup.show("회원가입 실패")

            self.view.screen.fill((255, 255, 255))

            color1 = color_active if active == 0 else color_inactive
            color2 = color_active if active == 1 else color_inactive

            pygame.draw.rect(self.view.screen, color1, input_box1, 2)
            pygame.draw.rect(self.view.screen, color2, input_box2, 2)
            pygame.draw.rect(self.view.screen, color_inactive, register_button, 2)

            self.view.draw_text('ID:', input_box1, 'left_out')
            self.view.draw_text('Password:', input_box2, 'left_out')
            self.view.draw_text('Register', register_button)

            self.view.draw_text(username, input_box1, 'left_in')
            self.view.draw_text(password, input_box2, 'left_in')

            self.popup.draw(self.view.screen)

            pygame.display.flip()
            clock.tick(30)