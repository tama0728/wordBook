import random
import mysql.connector
from config import config


class ChoiceModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()
        self.used_ids = set()

    def get_random_words(self, count=4, exclude_used=False):
        if exclude_used and self.used_ids:
            format_strings = ','.join(['%s'] * len(self.used_ids))
            query = f"SELECT * FROM words WHERE id NOT IN ({format_strings}) ORDER BY RAND() LIMIT %s"
            params = (*self.used_ids, count)
        else:
            query = "SELECT * FROM words ORDER BY RAND() LIMIT %s"
            params = (count, )

        self.cursor.execute(query, params)
        words = self.cursor.fetchall()

        if exclude_used:
            self.used_ids.update(word[0] for word in words)

        return words

    def generate_question(self, mode='eng_to_kor'):
        rs_words = self.get_random_words(exclude_used=True)
        if mode == 'eng_to_kor':
            question_word = rs_words[0][1]#'word']
            correct_answer = rs_words[0][2]#["mean"]
            # rs_words에서 뜻만 가져와서 choices 리스트 생성
            choices = [mean for _, _, mean, _ in rs_words]  # 한글 뜻 #'mean'
        elif mode == 'kor_to_eng':
            question_word = rs_words[0][2]#["mean"]
            correct_answer = rs_words[0][1]#['word']
            # rs_words에서 뜻만 가져와서 choices 리스트 생성
            choices = [word for _, _, word, _ in rs_words]  # 영어 뜻
        else:
            raise ValueError("Invalid mode. Choose 'eng_to_kor' or 'kor_to_eng'.")

        random.shuffle(choices)
        return {
            'question': question_word,
            'choices': choices, #[4]지선다
            'answer': correct_answer
        }



