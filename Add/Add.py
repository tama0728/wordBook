import mysql.connector
import pandas as pd

from config import config

conn = mysql.connector.connect(**config)
cursor = conn.cursor(prepared=True)

df = pd.read_excel('../words.xls')


for i in range(len(df)):
    query = "INSERT INTO words (word, mean, lv) VALUES ('%s', '%s', %d)" % (df.iloc[i, 0], df.iloc[i, 1], (df.iloc[i, 2]))
    if i % 100 == 0:
        print(query)
    cursor.execute(query)
conn.commit()
conn.close()
cursor.close()
