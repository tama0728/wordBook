import mysql.connector
from config import config

class WordCard:
    def __init__(self, word, mean, level, is_favorite=False):
        self.word = word
        self.mean = mean
        self.level = level
        self.is_favorite = is_favorite

class WordCardModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def fetch_wordcards(self, filter_levels=None, id=None, only_favorites=False, only_wrong=False):
        filter_query = []
        if filter_levels:
            filter_query.append("lv IN ({})".format(",".join(map(str, filter_levels))))
        if only_favorites and id is not None:
            filter_query.append("word IN (SELECT word FROM favorite WHERE id = %s)")
        if only_wrong and id is not None:
            filter_query.append("word IN (SELECT word FROM wrong WHERE id = %s)")

        filter_query = " AND ".join(filter_query)
        if filter_query:
            filter_query = "WHERE " + filter_query

        query = f"SELECT word, mean, lv FROM words {filter_query}"
        self.cursor.execute(query, (id,) if (only_favorites or only_wrong) and id is not None else ())
        wordcards = [WordCard(word, mean, level) for word, mean, level in self.cursor.fetchall()]

        if id is not None and not only_favorites:
            self.cursor.execute("SELECT word FROM favorite WHERE id = %s", (id,))
            favorite_words = [row[0] for row in self.cursor.fetchall()]
            for wordcard in wordcards:
                wordcard.is_favorite = wordcard.word in favorite_words

        return wordcards

    def add_to_favorite(self, id, word):
        self.cursor.execute("INSERT INTO favorite (id, word) VALUES (%s, %s)", (id, word))
        self.conn.commit()

    def remove_from_favorite(self, id, word):
        self.cursor.execute("DELETE FROM favorite WHERE id = %s AND word = %s", (id, word))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()