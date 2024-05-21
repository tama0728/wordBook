import mysql.connector
from config import config

class WordCard:
    def __init__(self, word, mean):
        self.word = word
        self.mean = mean

class WordCardModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def fetch_wordcards(self, filter_levels=None):
        filter_query = ""
        if filter_levels:
            filter_query = " WHERE lv IN ({})".format(",".join(filter_levels))
        self.cursor.execute("SELECT word, mean FROM words" + filter_query)
        return [WordCard(word, mean) for word, mean in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.conn.close()