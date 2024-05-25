import mysql.connector
from config import config
import random
class Word:
    def __init__(self, word, mean):
        self.word = word
        self.mean = mean

class ShortAnswerTestModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def fetch_words(self, level):
        self.cursor.execute("SELECT word, mean FROM words WHERE lv = %s", (level,))
        words = [Word(word, mean) for word, mean in self.cursor.fetchall()]
        random.shuffle(words)  # 단어들을 랜덤하게 섞습니다.
        return words[:10]  # 10개의 랜덤 단어만 반환합니다.


    def close(self):
        self.cursor.close()
        self.conn.close()