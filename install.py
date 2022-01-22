import sqlite3
conn = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE zaga (id INTEGER PRIMARY KEY, name char(100) NOT NULL, qty REAL NOT NULL, dimensions REAL NOT NULL, dodano INTEGER, izbrisano INTEGER, project TEXT, status bool NOT NULL)")
conn.execute("CREATE TABLE vrtalka (id INTEGER PRIMARY KEY, name char(100) NOT NULL, qty REAL NOT NULL, dimensions REAL NOT NULL, dodano INTEGER, izbrisano INTEGER, project TEXT, status bool NOT NULL)")
conn.execute("CREATE TABLE vars (id INTEGER PRIMARY KEY, name char(100) NOT NULL, value REAL NOT NULL)")
conn.execute("INSERT INTO vars (name, value) VALUES ('pozicijaLNull',10.0),('pozicijaDNull',10.0),('pozicijaL',10.0),('pozicijaD',10.0),('orodjeL',10.0),('orodjeD',10.0),('hodL',10.0),('pocasnejePredKoncemHodaL',10.0),('hitrostPredKoncemHodaL',10.0),('hodD',10.0),('pocasnejePredKoncemHodaD',10.0),('hitrostPredKoncemHodaD',10.0),('povratekL',10.0),('povratekD',10.0),('povrtavanjeL',10.0),('povrtavanjeD',10.0)")
conn.commit()
