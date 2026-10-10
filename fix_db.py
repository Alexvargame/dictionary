import sqlite3
import os

DB = r"C:\Python_3_13\django\dictionary\dictionary\db_words.sqlite3"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("UPDATE words_verb SET preposition = NULL WHERE preposition = 'None'")
print("preposition fixed:", cur.rowcount)

cur.execute("UPDATE words_verb SET preposition_case = NULL WHERE preposition_case = 'None'")
print("preposition_case fixed:", cur.rowcount)

conn.commit()
conn.close()
print("Done.")