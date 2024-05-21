import os
import mysql.connector
import pygame
import sys
import random
from config import config

pygame.init()

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def fetch_word():
    cursor.execute("SELECT word, mean FROM words WHERE lv=1")
    return cursor.fetchall()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 나눔고딕 폰트 파일 경로
font_path = "NanumBarunGothic.ttf"
# 폰트 생성
font = pygame.font.Font(font_path, 32)

# 텍스트 입력 상자의 크기와 위치
input_rect = pygame.Rect(200, 530, 400, 40)

falling_words = []
input_text = ''
score = 0
lives = 3

heart_images = [
    pygame.image.load(os.path.join("pink_heart.png")),
    pygame.image.load(os.path.join("gray_heart.png"))
]

wave_image_path = os.path.join("wave.png")

def generate_word():
    word_list = fetch_word()
    word_info = random.choice(word_list)
    word = word_info[0]
    mean = word_info[1]
    if mean not in [word_info["text"] for word_info in falling_words]:
        falling_words.append({"text": mean, "word": word, "x": random.randint(0, screen_width - 50), "y": 0, "speed": random.randint(3, 4)})

def update_word_positions():
    global lives
    # 화면 아래에 이미지 그리기
    image = pygame.image.load(wave_image_path)
    image_rect = image.get_rect()
    image_rect.bottom = screen_height - 70
    screen.blit(image, image_rect)

    for word_info in falling_words:
        word_info["y"] += word_info["speed"]
        if word_info["y"] > screen_height - 100:
            falling_words.remove(word_info)
            lives -= 1

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(str(text), True, color)
    screen.blit(text_surface, (x, y))

def check_input():
    global input_text
    global score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_text = input_text.lower()
                for word_info in falling_words:
                    if input_text == word_info["word"]:
                        falling_words.remove(word_info)
                        input_text = ''
                        return True
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                if event.unicode.isalpha():
                    input_text += event.unicode

    return False

def draw_hearts():
    for i in range(3):
        heart_image = heart_images[0] if i < lives else heart_images[1]
        screen.blit(heart_image, (20 + i * 40, 20))

def game_over():
    global falling_words
    global input_text
    global score
    global lives

    game_over_text = font.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)

    total_score_text = font.render("Total Score: {}".format(score), True, BLACK)
    total_score_rect = total_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(total_score_text, total_score_rect)

    quit_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)
    pygame.draw.rect(screen, RED, quit_button_rect)
    quit_text = font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)

    restart_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 170, 200, 50)
    pygame.draw.rect(screen, GREEN, restart_button_rect)
    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif restart_button_rect.collidepoint(mouse_pos):
                    return True

def main():
    global input_text
    global score
    global lives
    input_text = ''
    score = 0
    lives = 3
    next_word_time = 0
    while True:
        if lives <= 0:
            if game_over():
                continue

        if check_input():
            score += 1

        if pygame.time.get_ticks() > next_word_time:
            generate_word()
            next_word_time = pygame.time.get_ticks() + random.randint(1000, 3000)

        screen.fill(WHITE)

        pygame.draw.rect(screen, GRAY, input_rect)
        draw_text(input_text, input_rect.x + 5, input_rect.y)

        update_word_positions()

        for word_info in falling_words:
            draw_text(word_info["text"], word_info["x"], word_info["y"])

        score_text = font.render("Score: {}".format(score), True, BLACK)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 50))

        draw_hearts()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()