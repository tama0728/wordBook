import os
import pygame
import sys
import mysql.connector
from config import config  # config.py에서 설정 가져오기

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("영어 단어장")

# 폰트 설정
font_large = pygame.font.Font("/System/Library/Fonts/AppleSDGothicNeo.ttc", 30)
font_small = pygame.font.Font("/System/Library/Fonts/AppleSDGothicNeo.ttc", 20)

# 별표 이미지 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
star_filled_image_path = os.path.join(current_dir, "star_filled.png")
star_empty_image_path = os.path.join(current_dir, "star_empty.png")

star_filled_image = pygame.image.load(star_filled_image_path)
star_filled_image = pygame.transform.scale(star_filled_image, (28, 28))

star_empty_image = pygame.image.load(star_empty_image_path)
star_empty_image = pygame.transform.scale(star_empty_image, (28, 28))

# 단어장 데이터
words_per_page = 10
favorite_status = {}  # favorite 상태를 저장할 딕셔너리

# 현재 페이지 초기화
current_page = 1

def get_total_pages(words_per_page):
    # 데이터베이스 연결 설정
    connection = mysql.connector.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    
    try:
        cursor = connection.cursor()
        # 총 단어 수를 계산하는 쿼리 실행
        sql = "SELECT COUNT(*) FROM words"
        cursor.execute(sql)
        total_words = cursor.fetchone()[0]
        total_pages = (total_words + words_per_page - 1) // words_per_page
        return total_pages
    finally:
        connection.close()

def get_word_data(page, words_per_page):
    # 데이터베이스 연결 설정
    connection = mysql.connector.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    
    try:
        cursor = connection.cursor(dictionary=True)
        # 쿼리 실행
        sql = f"SELECT word, mean, lv FROM words LIMIT {words_per_page} OFFSET {(page - 1) * words_per_page}"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # favorite 상태 초기화
        for i, word in enumerate(result):
            # 가상의 ID를 사용하여 favorite 상태 초기화
            word_id = (page - 1) * words_per_page + i + 1
            if word_id not in favorite_status:
                favorite_status[word_id] = False
            word['id'] = word_id
        
        return result
    finally:
        connection.close()

def draw_text_centered(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_buttons():
    next_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 100, 40)
    prev_button = pygame.Rect(50, SCREEN_HEIGHT - 50, 100, 40)
    
    pygame.draw.rect(screen, (200, 200, 200), next_button)
    pygame.draw.rect(screen, (200, 200, 200), prev_button)
    
    draw_text_centered(screen, "Next", font_large, pygame.Color('black'), next_button)
    draw_text_centered(screen, "Prev", font_large, pygame.Color('black'), prev_button)

    return next_button, prev_button

def display_page(page):
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채움

    # 헤더 텍스트 그리기
    headers = ["No.", "단어", "뜻", "Lv."]
    header_positions = [(125, 50), (260, 50), (470, 50), (615, 50)]
    for header, pos in zip(headers, header_positions):
        header_text = font_large.render(header, True, pygame.Color('black'))
        header_rect = header_text.get_rect(center=pos)
        screen.blit(header_text, header_rect)

    # 데이터베이스에서 단어 데이터 가져오기
    word_data = get_word_data(page, words_per_page)

    # 단어 표시
    for i, word in enumerate(word_data):
        text_y = 100 + i * 70
        star_image = star_filled_image if favorite_status[word['id']] else star_empty_image
        screen.blit(star_image, (50, text_y))  # 별 이미지 표시
        
        # 각 열의 사각형 그리기
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(100, text_y, 50, 40))  # 인덱스 열
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(160, text_y, 200, 40))  # 단어 열
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(370, text_y, 200, 40))  # 뜻 열
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(580, text_y, 70, 40))  # 수준 열

        # 텍스트 렌더링
        index_text = font_large.render(str(word['id']), True, pygame.Color('black'))
        word_text = font_large.render(word['word'], True, pygame.Color('black'))
        meaning_text = font_small.render(word['mean'], True, pygame.Color('black')) if len(word['mean']) > 5 else font_large.render(word['mean'], True, pygame.Color('black'))
        
        # 수준 텍스트 결정
        level_text_str = ""
        if word['lv'] == 1:
            level_text_str = "초급"
        elif word['lv'] == 2:
            level_text_str = "중급"
        elif word['lv'] == 3:
            level_text_str = "고급"
        level_text = font_large.render(level_text_str, True, pygame.Color('black'))

        # 텍스트의 위치 설정
        index_text_rect = index_text.get_rect(center=(125, text_y + 20))
        word_text_rect = word_text.get_rect(center=(260, text_y + 20))
        meaning_text_rect = meaning_text.get_rect(center=(470, text_y + 20))
        level_text_rect = level_text.get_rect(center=(615, text_y + 20))

        # 화면에 텍스트 그리기
        screen.blit(index_text, index_text_rect)
        screen.blit(word_text, word_text_rect)
        screen.blit(meaning_text, meaning_text_rect)
        screen.blit(level_text, level_text_rect)

    # 페이지 전환 버튼 그리기
    next_button, prev_button = draw_buttons()
    
    pygame.display.flip()  # 화면을 업데이트
    return next_button, prev_button

def handle_click(mouse_x, mouse_y, next_button, prev_button):
    global current_page
    if 50 <= mouse_x <= 78:  # 별표 클릭 영역
        for i in range(words_per_page):
            text_y = 100 + i * 70
            if text_y <= mouse_y <= text_y + 28:
                word_id = (current_page - 1) * words_per_page + i + 1
                favorite_status[word_id] = not favorite_status[word_id]
                display_page(current_page)
                break
    elif prev_button.collidepoint(mouse_x, mouse_y):  # 이전 페이지 버튼
        if current_page > 1:
            current_page -= 1
            display_page(current_page)
    elif next_button.collidepoint(mouse_x, mouse_y):  # 다음 페이지 버튼
        if current_page < total_pages:
            current_page += 1
            display_page(current_page)

# 총 페이지 수 계산
total_pages = get_total_pages(words_per_page)

# 초기 페이지 표시
next_button, prev_button = display_page(current_page)

# 이벤트 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            handle_click(mouse_x, mouse_y, next_button, prev_button)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if current_page > 1:
                    current_page -= 1
                    next_button, prev_button = display_page(current_page)
            elif event.key == pygame.K_RIGHT:
                if current_page < total_pages:
                    current_page += 1
                    next_button, prev_button = display_page(current_page)
