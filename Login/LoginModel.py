import mysql.connector

from config import config


class LoginModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        # password = sha256(password.encode('utf-8')).hexdigest()
        query = "SELECT id FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        res = self.cursor.fetchone()
        if res is not None:
            return res[0]
        else:
            return False

    def get_admin(self, id):
        query = "SELECT admin FROM users WHERE id = %d" % id
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
