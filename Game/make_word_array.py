import mysql.connector
import random

# config.py에서 데이터베이스 구성 정보 가져오기
from config import config

# 데이터베이스에 연결하고 데이터 가져오기
def fetch_words():
    # MySQL 연결
    connection = mysql.connector.connect(**config)

    try:
        with connection.cursor(dictionary=True) as cursor:
            # 실행할 SQL 쿼리 작성
            sql = "SELECT word, mean FROM words"  # words 테이블에서 word와 mean 컬럼 선택

            # SQL 쿼리 실행
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            return result

    finally:
        connection.close()

def generate_word_pairs(num_pairs):
    # 입력받은 개수만큼 랜덤하게 선택
    data = fetch_words()
    if num_pairs > len(data):
        raise ValueError(f"Cannot provide {num_pairs} pairs. Maximum is {len(data)}.")

    selected_pairs = [(pair['word'], pair['mean']) for pair in random.sample(data, num_pairs)]

    return selected_pairs

def create_translation_dict(tuple_list):
    translation_dict = {}
    for korean_word, english_word in tuple_list:
        translation_dict[korean_word] = english_word
    return translation_dict