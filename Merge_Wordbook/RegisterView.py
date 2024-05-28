import pygame

from Button import Button
from View import View


class RegisterView:
    def __init__(self, view: View):
        self.register_button = Button(pygame.Rect(200, 350, 280, 50), "회원가입")

        self.id_box = pygame.Rect(200, 200, 280, 32)
        self.password_box = pygame.Rect(200, 250, 280, 32)
        self.phone_box = pygame.Rect(200, 300, 280, 32)
