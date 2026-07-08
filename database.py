import sqlite3

connection = sqlite3.connect("rentwise.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    location TEXT NOT NULL,

    price INTEGER,

    bedrooms INTEGER,

    bathrooms INTEGER,

    description TEXT,

    image TEXT

)
""")

connection.commit()
connection.close()

print("Database created successfully!")