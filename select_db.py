import sqlite3

conn = sqlite3.connect('flats.db')

c = conn.cursor()

# Create table
c.execute('''SELECT * FROM flats WHERE id = 480805''')
c.execute('''SELECT * FROM flats''')
for flat in c.fetchall():
    print(flat)

# c.execute('''ALTER TABLE flats
# ADD notification_sent INTEGER''')
#
# c.execute('''ALTER TABLE flats
# ADD email_sent INTEGER''')
c.close()