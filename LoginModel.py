import mysql.connector
from config import config

class LoginModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone() is not None

    def get_admin(self, username):
        query = "SELECT admin FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False

    def get_user_id(self, username):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None