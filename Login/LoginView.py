import pygame

from Api.Button import Button
from View import View


class LoginView:
    def __init__(self, view: View):
        self.login_button = Button(pygame.Rect(200, 320, 130, 50), "로그인", (0, 255, 0))
        self.register_button = Button(pygame.Rect(350, 320, 130, 50), "회원가입")

        self.id_box = pygame.Rect(200, 200, 280, 32)
        self.password_box = pygame.Rect(200, 250, 280, 32)
