import mysql.connector

from config import config


# 데이터베이스에 연결하고 데이터 가져오기
def fetch_words():
    # MySQL 연결
    connection = mysql.connector.connect(**config)

    try:
        with connection.cursor() as cursor:
            # 실행할 SQL 쿼리 작성
            sql = "SELECT * FROM words"  # words 테이블에서 모든 데이터를 선택

            # SQL 쿼리 실행
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            return result

    finally:
        connection.close()


# 데이터 가져오기 예제 실행
if __name__ == "__main__":
    data = fetch_words()
    for row in data:
        print(row)