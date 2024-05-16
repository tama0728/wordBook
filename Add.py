import mysql.connector
from config import config
import pandas as pd

conn = mysql.connector.connect(**config)
cursor = conn.cursor(prepared=True)

df = pd.read_excel('words.xls')


for i in range(len(df)):
    query = "INSERT INTO words (word, mean, lv) VALUES ('%s', '%s', %d)" % (df.iloc[i, 1], df.iloc[i, 2], (df.iloc[i, 3]))
    cursor.execute(query)
conn.commit()
conn.close()
cursor.close()
