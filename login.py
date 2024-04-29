import pygame
import mysql.connector
from pygame.locals import *
from config import config
from hashlib import sha256


class Model:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone() is not None

    def register(self, username, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (username, password))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("에러:", err)
            return False


class View:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("로그인")
        self.font = pygame.font.Font(None, 32)
        self.text_color = pygame.Color('black')
        self.register_button = pygame.Rect(350, 320, 130, 50)  # 회원가입 버튼 추가

    def draw_text(self, text, rect, where='center'):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        if where == 'center':
            text_rect.center = rect.center
        elif where == 'left_out':
            text_rect.centery = rect.centery
            text_rect.x = rect.x - text_rect.width - 3
        elif where == 'left_in':
            text_rect.centery = rect.centery
            text_rect.x = rect.left + 3
        self.screen.blit(text_surface, text_rect)

    def draw_register_button(self):  # 회원가입 버튼 그리기
        pygame.draw.rect(self.screen, (0, 255, 0), self.register_button)
        self.draw_text('Register', self.register_button)


class RegisterView:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("회원가입")
        self.font = pygame.font.Font(None, 32)
        self.text_color = pygame.Color('black')

    def draw_text(self, text, rect, where='center'):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        if where == 'center':
            text_rect.center = rect.center
        elif where == 'left_out':
            text_rect.centery = rect.centery
            text_rect.x = rect.x - text_rect.width - 3
        elif where == 'left_in':
            text_rect.centery = rect.centery
            text_rect.x = rect.left + 3
        self.screen.blit(text_surface, text_rect)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        clock = pygame.time.Clock()
        username = ''
        password = ''
        input_box1 = pygame.Rect(200, 200, 280, 32)
        input_box2 = pygame.Rect(200, 250, 280, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = None

        login_button = pygame.Rect(200, 320, 130, 50)

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
                            if self.model.login(username, password):
                                print("로그인 성공")
                            else:
                                print("로그인 실패")
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
                        if self.model.login(username, password):
                            print("로그인 성공")
                        else:
                            print("로그인 실패")
                        username = ''
                        password = ''
                    elif self.view.register_button.collidepoint(event.pos):  # 회원가입 버튼 클릭 처리
                        register_model = Model()
                        register_view = RegisterView()
                        register_controller = RegisterController(register_model, register_view)
                        register_controller.run()
                        pygame.display.set_caption("로그인")  # 다시 로그인 화면으로 돌아올 때 제목 변경
                        self.view.screen.fill((255, 255, 255))  # 다시 로그인 화면으로 돌아올 때 화면 초기화

            self.view.screen.fill((255, 255, 255))

            color1 = color_active if active == 0 else color_inactive
            color2 = color_active if active == 1 else color_inactive

            pygame.draw.rect(self.view.screen, color1, input_box1, 2)
            pygame.draw.rect(self.view.screen, color2, input_box2, 2)
            pygame.draw.rect(self.view.screen, color_inactive, login_button, 2)

            self.view.draw_text('ID:', input_box1, 'left_out')
            self.view.draw_text('Password:', input_box2, 'left_out')
            self.view.draw_text('Login', login_button)

            self.view.draw_text(username, input_box1, 'left_in')
            self.view.draw_text(password, input_box2, 'left_in')
            self.view.draw_register_button()  # 회원가입 버튼 그리기

            pygame.display.flip()
            clock.tick(30)


class RegisterController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

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
                            done = True  # 회원가입 성공 후 종료
                        else:
                            print("회원가입 실패")

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

            pygame.display.flip()
            clock.tick(30)


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run()


if __name__ == '__main__':
    main()
