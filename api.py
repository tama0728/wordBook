import pymysql.connector  # mysql과 연결하기 위한 커넥터
from pymysql.connector import Error  # 연결 에러시 처리하기 위한 라이브러리
from config.dbconfig import dbConfig  # 아래의 커넥터의 변수처리


def get_mysql_connection():
    try:

        connection = mysql.connector.connect(**dbConfig)

        if connection.is_connected():
            print('connection ok!')
            return connection

    except Error as e:
        print('Error while connecting to MySQL', e)
        return None