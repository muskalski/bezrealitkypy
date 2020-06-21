import sqlite3

conn = sqlite3.connect('flats.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE flats (id INTEGER PRIMARY KEY, is_new INTEGER, layout TEXT, size REAL, description TEXT,
# price REAL, status TEXT, district TEXT, added TEXT, updated TEXT, notification_sent INTEGER, email_sent INTEGER)''')

# c.execute('''ALTER TABLE flats
# ADD notification_sent INTEGER''')
#
# c.execute('''ALTER TABLE flats
# ADD email_sent INTEGER''')


c.execute('''ALTER TABLE flats
ADD description_pl TEXT''')
c.close()