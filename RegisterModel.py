import mysql.connector
from config import config
from hashlib import sha256


class RegisterModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def register(self, username, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (username, password))
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
            return True
        except mysql.connector.Error as err:
            print("에러:", err)
            return False
