import sqlite3

conn = sqlite3.connect('flats.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE flats (id INTEGER, is_new INTEGER, layout TEXT, size REAL, description TEXT, price REAL, 
status TEXT, district TEXT, added TEXT, updated TEXT)''')
