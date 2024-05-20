import mysql.connector
from config import config


def edit_word(word, new_word, new_mean, new_lv):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE words SET word = '%s', mean = '%s', lv = %d WHERE word = '%s'" % (new_word, new_mean, new_lv, word)

    try:
        cursor.execute(query)
    except:
        conn.close()
        cursor.close()
        return False

    conn.commit()
    conn.close()
    return True
