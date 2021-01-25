import sqlite3 

conn = sqlite3.connect('data.db')
cur = conn.cursor()

create_stock = 'CREATE TABLE IF NOT EXISTS stock (name TEXT, max_speed REAL, distance REAL, handler TEXT, stock TEXT)'
cur.execute(create_stock)

create_users = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
cur.execute(create_users)

conn.commit()
conn.close()