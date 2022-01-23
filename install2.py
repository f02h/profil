import sqlite3
conn = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE profili (id INTEGER PRIMARY KEY, name char(100) NOT NULL)")
conn.execute("INSERT INTO profili (name) VALUES ('profil_20x20'),('profil_30x30')")
conn.commit()
