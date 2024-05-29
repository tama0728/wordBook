import mysql.connector
import pygame

from BasicWordbook.BasicWordbookModel import BasicWordbookModel
from BasicWordbook.BasicWordbookView import BasicWordbookView
from config import config


class BasicWordbookController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.view = BasicWordbookView()
        self.model = BasicWordbookModel(user_id, self.view)
        self.search_active = False
        self.search_result = []
        self.done = False

    def display_page(self, page):
        filters = self.model.get_filters()
        word_data = self.search_result if self.search_active else self.model.get_word_data(page, filters)
        total_pages = 1 if self.search_active else self.model.get_total_pages(filters)
        self.view.display_page(page, word_data, total_pages, self.model.favorite_status, self.model.checkboxes)

    def handle_click(self, mouse_x, mouse_y):
        for i, checkbox in enumerate(self.model.checkboxes):
            if checkbox.is_collide((mouse_x, mouse_y)):
                self.model.toggle_checkbox(i)
                self.model.current_page = 1
                if self.search_active:
                    self.search_word()
                else:
                    self.display_page(self.model.current_page)
                return

        if self.view.home_button_rect.collidepoint(mouse_x, mouse_y):
            self.done = True
            return

        if self.view.prev_button.is_collide((mouse_x, mouse_y)):
            if self.model.current_page > 1:
                self.model.current_page -= 1
                self.display_page(self.model.current_page)
            return

        if self.view.next_button.is_collide((mouse_x, mouse_y)):
            if self.model.current_page < self.model.get_total_pages(self.model.get_filters()):
                self.model.current_page += 1
                self.display_page(self.model.current_page)
            return

        if self.view.search_button.is_collide((mouse_x, mouse_y)):
            self.search_word()
            return

        word_data = self.search_result if self.search_active else self.model.get_word_data(self.model.current_page,
                                                                                           self.model.get_filters())
        for i in range(self.model.words_per_page):
            text_y = 200 + i * 60
            star_rect = pygame.Rect(60, text_y, 20, 20)
            if star_rect.collidepoint(mouse_x, mouse_y) and i < len(word_data):
                word = word_data[i]
                word_id = word['id']
                self.model.favorite_status[word_id] = not self.model.favorite_status[word_id]
                self.model.update_favorite_status(word_id, word['word'], self.model.favorite_status[word_id])
                if self.search_active:
                    self.update_search_result_favorite_status(word_id)
                self.display_page(self.model.current_page)
                break

    def update_search_result_favorite_status(self, word_id):
        for word in self.search_result:
            if word['id'] == word_id:
                word['favorite'] = self.model.favorite_status[word_id]
                break

    def search_word(self):
        word = self.view.search_box.get_content()
        if word:
            connection = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            try:
                cursor = connection.cursor(dictionary=True)
                filters = self.model.get_filters()
                query = "SELECT * FROM words WHERE word LIKE %s"
                params = [f"%{word}%"]

                if filters["즐겨찾기"]:
                    query += " AND word IN (SELECT word FROM favorite WHERE id = %s)"
                    params.append(self.user_id)

                if filters["틀린 단어"]:
                    query += " AND word IN (SELECT word FROM wrong WHERE id = %s)"
                    params.append(self.user_id)

                lv_clauses = []
                if filters["초급"]:
                    lv_clauses.append("lv = 1")
                if filters["중급"]:
                    lv_clauses.append("lv = 2")
                if filters["고급"]:
                    lv_clauses.append("lv = 3")
                if lv_clauses:
                    query += " AND (" + " OR ".join(lv_clauses) + ")"

                cursor.execute(query, tuple(params))
                self.search_result = cursor.fetchall()

                for word in self.search_result:
                    word_id = word['id']
                    word['favorite'] = self.model.favorite_status[word_id]

                self.search_active = True
                self.model.current_page = 1
                self.display_page(self.model.current_page)

            finally:
                connection.close()
        else:
            self.search_active = False
            self.display_page(self.model.current_page)

    def run(self):
        while not self.done:
            self.view.screen.fill((255, 255, 255))
            self.display_page(self.model.current_page)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.handle_click(mouse_x, mouse_y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.search_word()
                    self.view.search_box.handle_input(event)

            pygame.display.flip()
