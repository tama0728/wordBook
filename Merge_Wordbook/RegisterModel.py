import mysql.connector

from config import config


class RegisterModel:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def register(self, username, password, phone):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor(prepared=True)
        query = "INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)"
        params = (username, password, phone)
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            self.conn.close()
            return True
        except mysql.connector.Error as err:
            print("에러:", err)
            self.conn.close()
            return False
