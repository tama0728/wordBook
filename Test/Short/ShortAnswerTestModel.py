import mysql.connector
from config import config


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
        if "Level" in filter_levels:
            filter_query = f"where lv = {filter_levels[-1]}"
        elif "favorites" in filter_levels:
            filter_query = ("word IN (SELECT word FROM favorite WHERE id = %d)" % user_id)
        else:
            filter_query = ("word IN (SELECT word FROM wrong WHERE id = %d)" % user_id)

        query = f"SELECT word, mean, lv FROM words {filter_query} ORDER BY RAND() LIMIT {limit}"
        self.cursor.execute(query)
        wordcards = self.cursor.fetchall()
        return wordcards

    def save_wrong_answer(self, user_id, word):
        query = "INSERT INTO wrong (id, word) VALUES (%d, '%s')" % (user_id, word)
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
