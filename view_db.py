# view_db.py
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()

print("Saved User Entries:\n--------------------")
for row in rows:
    user_id, email, phone = row
    print(f"ID: {user_id} | Email: {email} | Phone: {phone}")

conn.close()
