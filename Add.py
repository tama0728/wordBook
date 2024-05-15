import mysql.connector
from config import config
import pandas as pd

conn = mysql.connector.connect(**config)
cursor = conn.cursor(prepared=True)

df = pd.read_excel('words.xls')


for i in range(len(df)):
    query = "INSERT INTO words (word, mean, lv) VALUES (%s, %s, %s)"
    cursor.execute(query, (df.iloc[i, 1], df.iloc[i, 2], chr(df.iloc[i, 3])))
conn.commit()
conn.close()
cursor.close()
