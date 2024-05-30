import mysql.connector
from config import config
import random


class ShortAnswerTestCard:
    def __init__(self, word, mean, level, is_favorite=False):
        self.word = word
        self.mean = mean
        self.level = level
        self.is_favorite = is_favorite


class ShortAnswerTestModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def fetch_wordcards(self, limit=20, filter_levels=None, user_id=None):
        wordcards = []
        if "Level" in filter_levels:
            filter_query = f"where lv = {filter_levels[-1]}"
            query = f"SELECT word, mean, lv FROM words {filter_query} ORDER BY RAND() LIMIT {limit}"
            self.cursor.execute(query)
            wordcards = self.cursor.fetchall()

        elif "Favorites" in filter_levels:
            filter_query = "SELECT word FROM favorite WHERE id = %d" % user_id
            self.cursor.execute(filter_query)
            favorite_words = self.cursor.fetchall()
            if len(favorite_words) > limit:
                favorite_words = random.sample(favorite_words, limit)
            for word in favorite_words:
                query = f"SELECT word, mean, lv FROM words WHERE word = '{word[0]}'"
                self.cursor.execute(query)
                wordcards.append(self.cursor.fetchone())
        else:
            filter_query = "SELECT word FROM wrong WHERE id = %d" % user_id
            self.cursor.execute(filter_query)
            wrong_words = self.cursor.fetchall()
            if len(wrong_words) > limit:
                wrong_words = random.sample(wrong_words, limit)
            for word in wrong_words:
                query = f"SELECT word, mean, lv FROM words WHERE word = '{word[0]}'"
                self.cursor.execute(query)
                wordcards.append(self.cursor.fetchone())

        return wordcards

    def save_wrong_answer(self, user_id, word):
        # check if the word is already in the wrong table
        query = f"SELECT * FROM wrong WHERE id = {user_id} AND word = '{word}'"
        self.cursor.execute(query)
        if self.cursor.fetchone():
            return
        query = "INSERT INTO wrong (id, word) VALUES (%d, '%s')" % (user_id, word)
        self.cursor.execute(query)
        self.conn.commit()

    def delet_wrong_answer(self, user_id, word):
        # check if the word is not in the wrong table
        query = f"SELECT * FROM wrong WHERE id = {user_id} AND word = '{word}'"
        self.cursor.execute(query)
        if not self.cursor.fetchone():
            return
        query = "DELETE FROM wrong WHERE id = %d AND word = '%s'" % (user_id, word)
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
