import mysql.connector
from config import config
from hashlib import sha256

class Model:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone() is not None

    def register(self, username, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (username, password))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("에러:", err)
            return False
