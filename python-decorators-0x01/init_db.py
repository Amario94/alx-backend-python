# # init_db.py
# import sqlite3

# def initialize_database():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()

#     # Create users table if it doesn't exist
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL
#         )
#     ''')

#     # Optional: Only insert if table is empty
#     cursor.execute('SELECT COUNT(*) FROM users')
#     if cursor.fetchone()[0] == 0:
#         cursor.executemany('''
#             INSERT INTO users (name, email) VALUES (?, ?)
#         ''', [
#             ("Alice", "alice@example.com"),
#             ("Bob", "bob@example.com"),
#             ("Charlie", "charlie@example.com"),
#         ])

#     conn.commit()
#     conn.close()

import sqlite3
import csv
import os

def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # ✅ Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER
        )
    ''')

    # ✅ Add 'age' column if missing
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'age' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
        print("✅ 'age' column added.")
    else:
        print("ℹ️ 'age' column already exists.")

    # ✅ Process CSV
    csv_file = 'user_data.csv'
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            updated = 0
            inserted = 0
            for row in reader:
                try:
                    name = row['name'].strip()
                    email = row['email'].strip()
                    age = int(row['age'])

                    # Check if user exists by email
                    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                    result = cursor.fetchone()

                    if result:
                        cursor.execute("UPDATE users SET age = ?, name = ? WHERE email = ?", (age, name, email))
                        updated += 1
                    else:
                        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", (name, email, age))
                        inserted += 1
                except (KeyError, ValueError):
                    continue  # Skip malformed rows

            print(f"✅ {updated} users updated, {inserted} new users inserted.")
    else:
        print("❌ user_data.csv not found.")

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    initialize_database()
