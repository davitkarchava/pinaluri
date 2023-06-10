import sqlite3

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE info
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     username VARCHAR(100),
     password VARCHAR(100);
     """)

conn.commit()
conn.close()