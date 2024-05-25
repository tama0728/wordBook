import mysql.connector

from config import config


class LoginModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        # password = sha256(password.encode('utf-8')).hexdigest()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone() is not None

    def get_admin(self, username):
        query = "SELECT admin FROM users WHERE username = '%s'" % username
        res = self.cursor.execute(query)
        return self.cursor.fetchone()[0] == 1
