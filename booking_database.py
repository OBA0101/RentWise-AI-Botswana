import sqlite3

connection = sqlite3.connect("rentwise.db")
cursor = connection.cursor()

# Delete the old bookings table
cursor.execute("DROP TABLE IF EXISTS bookings")

# Create a new bookings table
cursor.execute("""
CREATE TABLE bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    property_id INTEGER NOT NULL,

    fullname TEXT NOT NULL,

    email TEXT NOT NULL,

    phone TEXT NOT NULL,

    viewing_date TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(property_id)
    REFERENCES properties(id)

)
""")

connection.commit()
connection.close()

print("Bookings table created successfully!")