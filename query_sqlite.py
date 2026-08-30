import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Query transactions
try:
    cursor.execute("SELECT id, sender_id, receiver_id, amount, description, transaction_type, status, timestamp FROM banking_transaction ORDER BY id DESC LIMIT 10;")
    rows = cursor.fetchall()
    print("\nRecent Transactions:")
    for row in rows:
        print(row)
except Exception as e:
    print("Error querying banking_transaction:", e)

conn.close()
