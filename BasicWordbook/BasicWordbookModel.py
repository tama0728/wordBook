from collections import defaultdict

import mysql.connector
import pygame

from Api.CheckBox import CheckBox
from config import config


class BasicWordbookModel:
    def __init__(self, user_id, view):
        self.user_id = user_id
        self.view = view
        self.words_per_page = 10
        self.favorite_status = defaultdict(lambda: False)
        self.current_page = 1
        self.checkboxes = [
            CheckBox("즐겨찾기", self.view, pygame.Rect(70, 30, 20, 20)),
            CheckBox("틀린 단어", self.view, pygame.Rect(200, 30, 20, 20)),
            CheckBox("초급", self.view, pygame.Rect(350, 30, 20, 20)),
            CheckBox("중급", self.view, pygame.Rect(450, 30, 20, 20)),
            CheckBox("고급", self.view, pygame.Rect(550, 30, 20, 20))
        ]
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor(dictionary=True)
        self.load_favorite_status()

    def load_favorite_status(self):
        self.cursor.execute("SELECT word FROM favorite WHERE id = %s", (self.user_id,))
        favorites = self.cursor.fetchall()
        for favorite in favorites:
            word = favorite['word']
            self.cursor.execute("SELECT id FROM words WHERE word = %s", (word,))
            word_id = self.cursor.fetchone()['id']
            self.favorite_status[word_id] = True

    def get_total_pages(self, filters):
        sql = "SELECT COUNT(*) FROM words"
        where_clauses = []

        if filters["즐겨찾기"]:
            where_clauses.append(
                f"id IN (SELECT words.id FROM words JOIN favorite ON words.word = favorite.word WHERE favorite.id = '{self.user_id}')")

        if filters["틀린 단어"]:
            where_clauses.append(f"id IN (SELECT words.id FROM wrong WHERE id = '{self.user_id}')")

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

        self.cursor.execute(sql)
        total_words = self.cursor.fetchone()
        total_words = total_words['COUNT(*)'] if total_words else 0
        if total_words >= 1:
            total_pages = (total_words + self.words_per_page - 1) // self.words_per_page
        else:
            total_pages = 1
        return total_pages

    def get_word_data(self, page, filters):
        sql = "SELECT words.id, words.word, words.mean, words.lv FROM words"

        where_clauses = []

        if filters["즐겨찾기"]:
            where_clauses.append(f"words.word IN (SELECT word FROM favorite WHERE id = '{self.user_id}')")

        if filters["틀린 단어"]:
            where_clauses.append(f"words.word IN (SELECT word FROM wrong WHERE id = '{self.user_id}')")

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

        sql += f" LIMIT {self.words_per_page} OFFSET {(page - 1) * self.words_per_page}"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        for word in result:
            word_id = word['id']
            word['favorite'] = self.favorite_status[word_id]

        return result

    def update_favorite_status(self, word_id, word, is_favorite):
        if is_favorite:
            self.cursor.execute("INSERT INTO favorite (id, word) VALUES (%s, %s)", (self.user_id, word))
        else:
            self.cursor.execute("DELETE FROM favorite WHERE id = %s AND word = %s", (self.user_id, word))
        self.conn.commit()

    def get_filters(self):
        return {
            "즐겨찾기": self.checkboxes[0].checked,
            "틀린 단어": self.checkboxes[1].checked,
            "초급": self.checkboxes[2].checked,
            "중급": self.checkboxes[3].checked,
            "고급": self.checkboxes[4].checked
        }

    def toggle_checkbox(self, checkbox_index):
        checkbox = self.checkboxes[checkbox_index]
        if checkbox.checked:
            checkbox.uncheck()
        else:
            checkbox.check()
