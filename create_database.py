import sqlite3 as sql

conn = sql.connect("database.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE messages (id_from text, id_to text, message text)")
conn.commit()

