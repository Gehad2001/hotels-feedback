import sqlite3
connection = sqlite3.connect('database.db')
with open('Tabels.sql','r') as f:
    cur = connection.cursor()
    cur.executescript(f.read())
connection.commit()
connection.close()
