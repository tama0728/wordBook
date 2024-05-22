import mysql.connector

from config import config


def add_word(word, mean, lv):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "INSERT INTO words (word, mean, lv) VALUES ('%s', '%s', %d)" % (word, mean, lv)

    try:
        cursor.execute(query)
    except:
        conn.close()
        cursor.close()
        return False
    conn.commit()
    conn.close()
    cursor.close()
    return True
