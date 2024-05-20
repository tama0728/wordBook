import mysql.connector
from config import config


def search(word):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "SELECT * FROM words WHERE word = '%s'" % word

    try:
        cursor.execute(query)
    except:
        conn.close()
        cursor.close()
        return False
    res = cursor.fetchone()
    if res is None:
        conn.close()
        cursor.close()
        return False
    else:
        conn.close()
        cursor.close()
        return [res[2], res[3]]
