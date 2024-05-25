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

    def fetch_wordcards(self, filter_levels=None, username=None, only_favorites=False):
        filter_query = []
        if filter_levels:
            filter_query.append("lv IN ({})".format(",".join(map(str, filter_levels))))
        if only_favorites and username:
            filter_query.append("word IN (SELECT word FROM favorite WHERE username = %s)")

        filter_query = " AND ".join(filter_query)
        if filter_query:
            filter_query = "WHERE " + filter_query

        query = f"SELECT word, mean, lv FROM words {filter_query}"
        self.cursor.execute(query, (username,) if only_favorites and username else ())
        wordcards = [WordCard(word, mean, level) for word, mean, level in self.cursor.fetchall()]

        if username and not only_favorites:
            self.cursor.execute("SELECT word FROM favorite WHERE username = %s", (username,))
            favorite_words = [row[0] for row in self.cursor.fetchall()]
            for wordcard in wordcards:
                wordcard.is_favorite = wordcard.word in favorite_words

        return wordcards

    def add_to_favorite(self, username, word):
        self.cursor.execute("INSERT INTO favorite (username, word) VALUES (%s, %s)", (username, word))
        self.conn.commit()

    def remove_from_favorite(self, username, word):
        self.cursor.execute("DELETE FROM favorite WHERE username = %s AND word = %s", (username, word))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()