import mysql.connector

from config import config


class CheckWriteRanking:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
            self.cursor.close()

    def get_user_scores(self, user_id):
        try:
            # 사용자 이름을 검색
            query = "SELECT username FROM users WHERE id = %d" % user_id
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            if user is None:
                return ["User not found", None, None]

            username = user[0]

            # users 테이블에서 카드 게임 점수 및 빗방울 게임 점수 검색
            query = "SELECT card_score, rain_score FROM users WHERE id = %d" % user_id
            self.cursor.execute(query)
            score_data = self.cursor.fetchone()
            card_score = score_data[0] if score_data else 0
            rain_score = score_data[1] if score_data else 0

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
            # game_rain 테이블에서 상위 3명의 username과 score를 내림차순으로 가져옴
            query = "SELECT username, score FROM game_rain ORDER BY score DESC LIMIT 3"
            self.cursor.execute(query)
            return self.cursor.fetchall()  # 결과를 리스트 형태로 반환
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
            # game_card 테이블에서 상위 3명의 username과 score를 오름차순으로 가져옴
            query = "SELECT username, score FROM game_card ORDER BY score ASC LIMIT 3"
            self.cursor.execute(query)
            return self.cursor.fetchall()  # 결과를 리스트 형태로 반환
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def update_rain_ranking(self, id, username, score):
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
        if len(current_ranking) < 3 or score > current_ranking[-1][1]:
            try:
                # 새로운 점수를 추가함
                query = "INSERT INTO game_rain (id, username, score) VALUES (%d, '%s', %d)" % (id, username, score)
                self.cursor.execute(query)
                self.conn.commit()  # 변경 사항을 커밋함

                # 상위 3명의 점수를 다시 가져옴
                updated_ranking = self.get_current_rain_ranking()

                # 상위 3명의 점수만 유지하고 나머지 점수는 삭제
                if len(updated_ranking) > 3:
                    query = ("DELETE FROM game_rain WHERE (id, score) NOT IN (SELECT id, score FROM "
                             "(SELECT id, score FROM game_rain ORDER BY score DESC LIMIT 3) as top3)")
                    self.cursor.execute(query)
                    self.conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def update_card_ranking(self, id, username, score):
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
        if len(current_ranking) < 3 or score < current_ranking[-1][1]:
            try:
                # 새로운 점수를 추가함
                query = "INSERT INTO game_card (id, username, score) VALUES (%d, '%s', %d)" % (id, username, score)
                self.cursor.execute(query)
                self.conn.commit()  # 변경 사항을 커밋함

                # 상위 3명의 점수를 다시 가져옴
                updated_ranking = self.get_current_card_ranking()

                # 상위 3명의 점수만 유지하고 나머지 점수는 삭제
                if len(updated_ranking) > 3:
                    query = ("DELETE FROM game_card WHERE (id, score) NOT IN (SELECT id, score FROM "
                             "(SELECT id, score FROM game_card ORDER BY score ASC LIMIT 3) as top3)")
                    self.cursor.execute(query)
                    self.conn.commit()

            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def update_user_rain_score(self, id, new_rain_score):
        """
        주어진 사용자 ID로 users 테이블을 검색하여 rain_score를 덮어씌움.

        Args:
            id (int): 사용자의 ID.
            new_rain_score (int): 새로운 rain_score 값.
        """
        try:
            # user_id를 사용하여 현재 사용자의 rain_score를 검색
            query = "SELECT rain_score FROM users WHERE id = %d" % id
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            result = result[0]

            if result is None:
                print(f"User with ID '{id}' not found in the database.")
                result = 0

            current_rain_score = result  # 현재 rain_score를 가져옴

            # 새로운 rain_score가 현재 rain_score보다 높을 때만 업데이트 수행
            if new_rain_score > current_rain_score:
                query = "UPDATE users SET rain_score = %d WHERE id = %d" % (new_rain_score, id)
                self.cursor.execute(query)
                self.conn.commit()  # 변경 사항을 커밋함
                print(f"Successfully updated rain_score for user with ID '{id}' to {new_rain_score}")
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
            # user_id를 사용하여 현재 사용자의 card_score를 검색
            query = "SELECT card_score FROM users WHERE id = %d" % user_id
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            result = result[0]

            if result is None:
                print(f"User with ID '{user_id}' not found in the database.")
                result = float('inf')

            current_card_score = result

            # 새로운 card_score가 현재 card_score보다 낮을 때만 업데이트 수행
            if new_card_score < current_card_score:
                query = "UPDATE users SET card_score = %d WHERE id = %d" % (new_card_score, user_id)
                self.cursor.execute(query)
                self.conn.commit()  # 변경 사항을 커밋함
                print(f"Successfully updated card_score for user with ID '{user_id}' to {new_card_score}")
            else:
                print(
                    f"New card_score ({new_card_score}) is not lower than current card_score ({current_card_score}). No update performed.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
