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

    def fetch_wordcards(self, limit=20, filter_levels=None, user_id=None, only_favorites=False, only_wrong=False):
        filter_query = []
        if filter_levels:
            levels = ",".join([str(level) for level in filter_levels])
            filter_query.append(f"lv IN ({levels})")
        if only_favorites and user_id is not None:
            filter_query.append("word IN (SELECT word FROM favorite WHERE id = %s)")
        if only_wrong and user_id is not None:
            filter_query.append("word IN (SELECT word FROM wrong WHERE id = %s)")

        filter_query = " AND ".join(filter_query)
        if filter_query:
            filter_query = "WHERE " + filter_query

        query = f"SELECT word, mean, lv FROM words {filter_query} ORDER BY RAND() LIMIT {limit}"
        self.cursor.execute(query, (user_id,) if (only_favorites or only_wrong) and user_id is not None else ())
        wordcards = [ShortAnswerTestCard(word, mean, level) for word, mean, level in self.cursor.fetchall()]

        if user_id is not None and not (only_favorites or only_wrong):
            self.cursor.execute("SELECT word FROM favorite WHERE id = %s", (user_id,))
            favorite_words = [row[0] for row in self.cursor.fetchall()]
            for wordcard in wordcards:
                wordcard.is_favorite = wordcard.word in favorite_words

        return wordcards

    def save_wrong_answer(self, user_id, word):
        query = "INSERT INTO wrong (id, word) VALUES (%s, %s)"
        self.cursor.execute(query, (user_id, word))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()