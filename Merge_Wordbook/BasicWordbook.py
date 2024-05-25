import os
import pygame
import sys
import mysql.connector
from collections import defaultdict
from CheckBox import CheckBox
from config import config
from Button import Button 

class BasicWordbook:
    def __init__(self, username):
        pygame.init()

        self.username = username
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("영어 단어장")

        self.font_large = pygame.font.SysFont("D2Coding", 20)
        self.font_small = pygame.font.SysFont("D2Coding", 15)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        star_filled_image_path = os.path.join(current_dir, "star_filled.png")
        star_empty_image_path = os.path.join(current_dir, "star_empty.png")

        self.star_filled_image = pygame.image.load(star_filled_image_path)
        self.star_filled_image = pygame.transform.scale(self.star_filled_image, (20, 20))

        self.star_empty_image = pygame.image.load(star_empty_image_path)
        self.star_empty_image = pygame.transform.scale(self.star_empty_image, (20, 20))

        self.words_per_page = 10
        self.favorite_status = defaultdict(lambda: False)

        self.current_page = 1
        self.total_pages = 1

        self.view_wrapper = self.ViewWrapper(self.screen)
        self.checkboxes = [
            CheckBox("즐겨찾기", self.view_wrapper, pygame.Rect(450, 50, 20, 20)),
            CheckBox("틀린 단어", self.view_wrapper, pygame.Rect(450, 80, 20, 20)),
            CheckBox("초급", self.view_wrapper, pygame.Rect(570, 50, 20, 20)),
            CheckBox("중급", self.view_wrapper, pygame.Rect(570, 80, 20, 20)),
            CheckBox("고급", self.view_wrapper, pygame.Rect(570, 110, 20, 20))
        ]

        for checkbox in self.checkboxes:
            def toggle(self):
                self.checked = not self.checked
            checkbox.toggle = toggle.__get__(checkbox, CheckBox)

        self.load_favorite_status()

        # 새로운 버튼들을 생성하고 리스트에 저장
        self.prev_button = Button(pygame.Rect(20, self.SCREEN_HEIGHT - 50, 80, 40), "이전")
        self.next_button = Button(pygame.Rect(600, self.SCREEN_HEIGHT - 50, 80, 40), "다음")

        self.buttons = [self.prev_button, self.next_button]

    class ViewWrapper:
        def __init__(self, screen):
            self.screen = screen

        def draw_text(self, text, rect, align, font_size):
            font = pygame.font.SysFont("d2coding", font_size)
            text_surface = font.render(text, True, (0, 0, 0))
            if align == 'left_out':
                text_rect = text_surface.get_rect(midleft=rect.midright)
            elif align == 'center':
                text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def load_favorite_status(self):
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT word FROM favorite WHERE username = %s", (self.username,))
            favorites = cursor.fetchall()
            for favorite in favorites:
                word = favorite[0]
                cursor.execute("SELECT id FROM words WHERE word = %s", (word,))
                word_id = cursor.fetchone()[0]
                self.favorite_status[word_id] = True
        finally:
            connection.close()

    def get_total_pages(self, filters):
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        try:
            cursor = connection.cursor()
            sql = "SELECT COUNT(*) FROM words"
            where_clauses = []

            if filters["즐겨찾기"]:
                where_clauses.append(f"id IN (SELECT words.id FROM words JOIN favorite ON words.word = favorite.word WHERE favorite.username = '{self.username}')")

            if filters["틀린 단어"]:
                where_clauses.append(f"id IN (SELECT words.id FROM wrong WHERE username = '{self.username}')")

            lv_clauses = []
            if filters["초급"]:
                lv_clauses.append("lv = 1")
            if filters["중급"]:
                lv_clauses.append("lv = 2")
            if filters["고급"]:
                lv_clauses.append("lv = 3")
            if lv_clauses:
                where_clauses.append(f"({' OR '.join(lv_clauses)})")

            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)

            cursor.execute(sql)
            total_words = cursor.fetchone()[0]
            total_pages = (total_words + self.words_per_page - 1) // self.words_per_page
            return total_pages
        finally:
            connection.close()

    def get_word_data(self, page, words_per_page, filters):
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        try:
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT words.id, words.word, words.mean, words.lv FROM words"
            
            where_clauses = []
            
            if filters["즐겨찾기"]:
                where_clauses.append(f"words.word IN (SELECT word FROM favorite WHERE username = '{self.username}')")

            if filters["틀린 단어"]:
                where_clauses.append(f"words.word IN (SELECT word FROM wrong WHERE username = '{self.username}')")

            lv_clauses = []
            if filters["초급"]:
                lv_clauses.append("words.lv = 1")
            if filters["중급"]:
                lv_clauses.append("words.lv = 2")
            if filters["고급"]:
                lv_clauses.append("words.lv = 3")
            if lv_clauses:
                where_clauses.append(f"({' OR '.join(lv_clauses)})")
            
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            
            sql += f" LIMIT {words_per_page} OFFSET {(page - 1) * words_per_page}"
            cursor.execute(sql)
            result = cursor.fetchall()
            
            for word in result:
                word_id = word['id']
                word['favorite'] = self.favorite_status[word_id]
            
            return result
        finally:
            connection.close()

    def draw_text_centered(self, surface, text, font, color, rect):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def display_page(self, page):
        self.screen.fill((255, 255, 255))

        headers = ["No.", "단어", "뜻", "Lv."]
        header_positions = [(120, 180), (240, 180), (430, 180), (560, 180)]
        for header, pos in zip(headers, header_positions):
            header_text = self.font_large.render(header, True, pygame.Color('black'))
            header_rect = header_text.get_rect(center=pos)
            self.screen.blit(header_text, header_rect)

        filters = self.get_filters()

        word_data = self.get_word_data(page, self.words_per_page, filters)
        self.total_pages = self.get_total_pages(filters)  # Update total pages based on filters

        for i, word in enumerate(word_data):
            text_y = 200 + i * 60
            star_image = self.star_filled_image if word['favorite'] else self.star_empty_image
            star_rect = pygame.Rect(60, text_y, 20, 20)
            self.screen.blit(star_image, star_rect)
            
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(100, text_y, 40, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(150, text_y, 180, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(340, text_y, 180, 30))
            pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(530, text_y, 60, 30))

            index_text = self.font_large.render(str((page - 1) * self.words_per_page + i + 1), True, pygame.Color('black'))
            word_text = self.font_large.render(word['word'], True, pygame.Color('black'))
            meaning_text = self.font_small.render(word['mean'], True, pygame.Color('black')) if len(word['mean']) > 5 else self.font_large.render(word['mean'], True, pygame.Color('black'))
            
            level_text_str = ""
            if word['lv'] == 1:
                level_text_str = "초급"
            elif word['lv'] == 2:
                level_text_str = "중급"
            elif word['lv'] == 3:
                level_text_str = "고급"
            level_text = self.font_large.render(level_text_str, True, pygame.Color('black'))

            index_text_rect = index_text.get_rect(center=(120, text_y + 15))
            word_text_rect = word_text.get_rect(center=(240, text_y + 15))
            meaning_text_rect = meaning_text.get_rect(center=(430, text_y + 15))
            level_text_rect = level_text.get_rect(center=(560, text_y + 15))

            self.screen.blit(index_text, index_text_rect)
            self.screen.blit(word_text, word_text_rect)
            self.screen.blit(meaning_text, meaning_text_rect)
            self.screen.blit(level_text, level_text_rect)

        # 새로운 버튼들을 화면에 그림
        for button in self.buttons:
            button.draw(self.screen)

        # 현재 페이지와 전체 페이지 표시
        page_info_text = f"{page} / {self.total_pages}"
        page_info_surface = self.font_large.render(page_info_text, True, pygame.Color('black'))
        page_info_rect = page_info_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(page_info_surface, page_info_rect)

        for checkbox in self.checkboxes:
            checkbox.draw()
        
        pygame.display.flip()
        return self.next_button, self.prev_button

    def update_favorite_status(self, word_id, word, is_favorite):
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        try:
            cursor = connection.cursor()
            if is_favorite:
                cursor.execute("INSERT INTO favorite (username, word) VALUES (%s, %s)", (self.username, word))
            else:
                cursor.execute("DELETE FROM favorite WHERE username = %s AND word = %s", (self.username, word))
            connection.commit()
        finally:
            connection.close()

    def handle_click(self, mouse_x, mouse_y):
        filters = self.get_filters()
        for checkbox in self.checkboxes:
            if checkbox.is_collide((mouse_x, mouse_y)):
                checkbox.toggle()
                self.current_page = 1  # 필터를 클릭하면 현재 페이지를 1로 설정
                self.display_page(self.current_page)
                return

        if self.prev_button.is_collide((mouse_x, mouse_y)):
            if self.current_page > 1:
                self.current_page -= 1
                self.display_page(self.current_page)
            return

        if self.next_button.is_collide((mouse_x, mouse_y)):
            if self.current_page < self.total_pages:
                self.current_page += 1
                self.display_page(self.current_page)
            return

        for i in range(self.words_per_page):
            text_y = 200 + i * 60
            star_rect = pygame.Rect(60, text_y, 20, 20)
            if star_rect.collidepoint(mouse_x, mouse_y):
                word_data = self.get_word_data(self.current_page, self.words_per_page, filters)
                word = word_data[i]
                word_id = word['id']
                self.favorite_status[word_id] = not self.favorite_status[word_id]
                self.update_favorite_status(word_id, word['word'], self.favorite_status[word_id])
                self.display_page(self.current_page)
                break

    def get_filters(self):
        return {
            "즐겨찾기": self.checkboxes[0].checked,
            "틀린 단어": self.checkboxes[1].checked,
            "초급": self.checkboxes[2].checked,
            "중급": self.checkboxes[3].checked,
            "고급": self.checkboxes[4].checked
        }

    def run(self):
        done = False
        while not done:
            self.screen.fill((255, 255, 255))

            self.display_page(self.current_page)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.handle_click(mouse_x, mouse_y)
                if event.type == pygame.MOUSEMOTION:
                    self.prev_button.is_hover(event.pos)
                    self.next_button.is_hover(event.pos)
