import pygame
import tkinter as tk
from tkinter import filedialog

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Excel 파일 선택")

clock = pygame.time.Clock()

# 버튼 관련 설정
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_TEXT = "파일 선택"
BUTTON_FONT = pygame.font.SysFont("d2coding", 30)


def draw_button(x, y, text, hover=False):
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))

    text_surface = BUTTON_FONT.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2))
    screen.blit(text_surface, text_rect)


def open_file_dialog():
    file_path = filedialog.askopenfilename()

    return file_path


running = True
hover_button = False
selected_file = None

while running:
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채움

    # 버튼 그리기
    button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) / 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) / 2, BUTTON_WIDTH,
                              BUTTON_HEIGHT)
    draw_button(button_rect.x, button_rect.y, BUTTON_TEXT, hover_button)

    pygame.display.flip()  # 화면 업데이트
    clock.tick(30)  # 초당 프레임 수를 30으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hover_button:
                selected_file = open_file_dialog()
                print("선택한 파일:", selected_file)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover_button = button_rect.collidepoint(mouse_x, mouse_y)


pygame.quit()
