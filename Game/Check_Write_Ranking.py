import mysql.connector
from config import config


class Check_Write_Ranking:
    def __init__(self):
        """
        클래스 초기화 및 MySQL 데이터베이스 연결.
        """
        self.connection = mysql.connector.connect(**config)

    def __del__(self):
        """
        객체 소멸 시 MySQL 데이터베이스 연결 해제.
        """
        if self.connection.is_connected():
            self.connection.close()

    def get_user_scores(self, user_id):
        """
        주어진 사용자 ID로 사용자 이름, 카드 게임 점수 및 빗방울 게임 점수를 검색하여 반환함.

        Args:
            user_id (int): 사용자의 ID.

        Returns:
            list: 사용자의 username, card_score, rain_score를 저장한 리스트.
        """
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                # 사용자 이름을 검색
                cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                if user is None:
                    return ["User not found", None, None]

                username = user['username']

                # users 테이블에서 카드 게임 점수 및 빗방울 게임 점수 검색
                cursor.execute("SELECT card_score, rain_score FROM users WHERE id = %s", (user_id,))
                score_data = cursor.fetchone()
                card_score = score_data['card_score'] if score_data else 0
                rain_score = score_data['rain_score'] if score_data else 0

            return [username, card_score, rain_score]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return ["Error", None, None]

    def get_current_rain_ranking(self):
        """
        현재 상위 3명의 사용자와 점수를 가져옴.

        Returns:
            list: 상위 3명의 사용자와 점수가 딕셔너리 형태로 저장된 리스트.
        """
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                # game_rain 테이블에서 상위 3명의 username과 score를 내림차순으로 가져옴
                cursor.execute("SELECT username, score FROM game_rain ORDER BY score DESC LIMIT 3")
                return cursor.fetchall()  # 결과를 리스트 형태로 반환
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_current_card_ranking(self):
        """
        현재 상위 3명의 사용자와 점수를 가져옴.

        Returns:
            list: 상위 3명의 사용자와 점수가 딕셔너리 형태로 저장된 리스트.
        """
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                # game_card 테이블에서 상위 3명의 username과 score를 오름차순으로 가져옴
                cursor.execute("SELECT username, score FROM game_card ORDER BY score ASC LIMIT 3")
                return cursor.fetchall()  # 결과를 리스트 형태로 반환
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def update_rain_ranking(self, username, score):
        """
        주어진 사용자 이름과 점수를 사용하여 순위를 업데이트.
        새로운 점수가 상위 3위 안에 들어가면 테이블을 업데이트함.

        Args:
            username (str): 사용자의 이름.
            score (int): 사용자의 점수.
        """
        # 현재 상위 3명의 점수를 가져옴
        current_ranking = self.get_current_rain_ranking()

        # 새로운 점수가 상위 3위 안에 들어갈 수 있는지 확인
        if len(current_ranking) < 3 or score > current_ranking[-1]['score']:
            try:
                with self.connection.cursor() as cursor:
                    # 새로운 점수를 추가함
                    cursor.execute("INSERT INTO game_rain (username, score) VALUES (%s, %s)",
                                   (username, score))
                    self.connection.commit()  # 변경 사항을 커밋함

                    # 상위 3명의 점수를 다시 가져옴
                    updated_ranking = self.get_current_rain_ranking()

                    # 상위 3명의 점수만 유지하고 나머지 점수는 삭제
                    if len(updated_ranking) > 3:
                        cursor.execute(
                            "DELETE FROM game_rain WHERE (username, score) NOT IN (SELECT username, score FROM (SELECT username, score FROM game_rain ORDER BY score DESC LIMIT 3) as top3)"
                        )
                        self.connection.commit()

            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def update_card_ranking(self, username, score):
        """
        주어진 사용자 이름과 점수를 사용하여 순위를 업데이트.
        새로운 점수가 상위 3위 안에 들어가면 테이블을 업데이트함.

        Args:
            username (str): 사용자의 이름.
            score (int): 사용자의 점수.
        """
        # 현재 상위 3명의 점수를 가져옴
        current_ranking = self.get_current_card_ranking()

        # 새로운 점수가 상위 3위 안에 들어갈 수 있는지 확인
        if len(current_ranking) < 3 or score < current_ranking[-1]['score']:
            try:
                with self.connection.cursor() as cursor:
                    # 새로운 점수를 추가함
                    cursor.execute("INSERT INTO game_card (username, score) VALUES (%s, %s)",
                                   (username, score))
                    self.connection.commit()  # 변경 사항을 커밋함

                    # 상위 3명의 점수를 다시 가져옴
                    updated_ranking = self.get_current_card_ranking()

                    # 상위 3명의 점수만 유지하고 나머지 점수는 삭제
                    if len(updated_ranking) > 3:
                        cursor.execute(
                            "DELETE FROM game_card WHERE (username, score) NOT IN (SELECT username, score FROM (SELECT username, score FROM game_card ORDER BY score ASC LIMIT 3) as top3)"
                        )
                        self.connection.commit()

            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def update_user_rain_score(self, user_id, new_rain_score):
        """
        주어진 사용자 ID로 users 테이블을 검색하여 rain_score를 덮어씌움.

        Args:
            user_id (int): 사용자의 ID.
            new_rain_score (int): 새로운 rain_score 값.
        """
        try:
            with self.connection.cursor() as cursor:
                # user_id를 사용하여 현재 사용자의 rain_score를 검색
                cursor.execute("SELECT rain_score FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()

                if result is None:
                    print(f"User with ID '{user_id}' not found in the database.")
                    return

                current_rain_score = result[0]  # 현재 rain_score를 가져옴

                # 새로운 rain_score가 현재 rain_score보다 높을 때만 업데이트 수행
                if new_rain_score > current_rain_score:
                    cursor.execute("UPDATE users SET rain_score = %s WHERE id = %s",
                                   (new_rain_score, user_id))
                    self.connection.commit()  # 변경 사항을 커밋함
                    print(f"Successfully updated rain_score for user with ID '{user_id}' to {new_rain_score}")
                else:
                    print(
                        f"New rain_score ({new_rain_score}) is not higher than current rain_score ({current_rain_score}). No update performed.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_user_card_score(self, user_id, new_card_score):
        """
        주어진 사용자 ID로 users 테이블을 검색하여 card_score를 덮어씌움.

        Args:
            user_id (int): 사용자의 ID.
            new_card_score (int): 새로운 card_score 값.
        """
        try:
            with self.connection.cursor() as cursor:
                # user_id를 사용하여 현재 사용자의 card_score를 검색
                cursor.execute("SELECT card_score FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()

                if result is None:
                    print(f"User with ID '{user_id}' not found in the database.")
                    return

                current_card_score = result[0]

                # current_card_score가 None인 경우 0으로 설정 (혹은 다른 기본값 설정)
                if current_card_score is None:
                    current_card_score = float('inf')

                # 새로운 card_score가 현재 card_score보다 낮을 때만 업데이트 수행
                if new_card_score < current_card_score:
                    cursor.execute("UPDATE users SET card_score = %s WHERE id = %s",
                                   (new_card_score, user_id))
                    self.connection.commit()  # 변경 사항을 커밋함
                    print(f"Successfully updated card_score for user with ID '{user_id}' to {new_card_score}")
                else:
                    print(
                        f"New card_score ({new_card_score}) is not lower than current card_score ({current_card_score}). No update performed.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
