import mysql.connector

from config import config


def del_word(word):
    if word == "":
        return False
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "DELETE FROM words WHERE word = '%s'" % word

    try:
        cursor.execute(query)
    except:
        conn.close()
        cursor.close()
        return False

    conn.commit()
    conn.close()
    return True
