import pygame
import mysql.connector
from pygame.locals import *
from config import config
from hashlib import sha256

# 화면 초기화
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("로그인")

# 폰트 설정
font = pygame.font.Font(None, 32)
text_color = pygame.Color('black')

# 데이터베이스 연결
conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def login(username, password):
    password = sha256(password.encode('utf-8')).hexdigest()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None


def register(username, password):
    password = sha256(password.encode('utf-8')).hexdigest()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, password))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("에러:", err)
        return False


def draw_text(surface, text, font, color, rect, where='center'):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if where == 'center':
        text_rect.center = rect.center
    elif where == 'left_out':
        text_rect.centery = rect.centery
        text_rect.x = rect.x - text_rect.width - 3
    elif where == 'left_in':
        text_rect.centery = rect.centery
        text_rect.x = rect.left + 3
    surface.blit(text_surface, text_rect)


def main():
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
                        if login(username, password):
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
                    if login(username, password):
                        print("로그인 성공")
                    else:
                        print("로그인 실패")
                    username = ''
                    password = ''
                elif register_button.collidepoint(event.pos):
                    if register(username, password):
                        print("회원가입 성공")
                    else:
                        print("회원가입 실패")
                    username = ''
                    password = ''
                else:
                    active = None
                    pass
        screen.fill((255, 255, 255))

        color1 = color_active if active == 0 else color_inactive
        color2 = color_active if active == 1 else color_inactive

        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)
        pygame.draw.rect(screen, color_inactive, login_button, 2)
        pygame.draw.rect(screen, color_inactive, register_button, 2)

        draw_text(screen, 'ID:', font, text_color, input_box1, 'left_out')
        draw_text(screen, 'Password:', font, text_color, input_box2, 'left_out')
        draw_text(screen, 'Login', font, text_color, login_button)
        draw_text(screen, 'Register', font, text_color, register_button)

        draw_text(screen, username, font, text_color, input_box1, 'left_in')
        draw_text(screen, password, font, text_color, input_box2, 'left_in')

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
