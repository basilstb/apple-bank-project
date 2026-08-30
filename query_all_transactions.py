import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("SELECT id, description FROM banking_transaction;")
rows = cursor.fetchall()
print("All Transactions:")
for row in rows:
    print(row)

conn.close()
