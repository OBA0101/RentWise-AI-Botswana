import sqlite3

connection = sqlite3.connect("rentwise.db")
cursor = connection.cursor()

properties = [
    (
        "Modern Apartment",
        "Gaborone",
        4500,
        2,
        1,
        "Beautiful apartment close to the city centre.",
        "images/apartment1.jpg"
    ),
    (
        "Family House",
        "Francistown",
        6800,
        3,
        2,
        "Perfect family home with a spacious yard.",
        "images/apartment2.jpg"
    ),
    (
        "Luxury Villa",
        "Maun",
        12000,
        5,
        4,
        "Luxury villa with swimming pool.",
        "images/apartment3.jpg"
    )
]

cursor.execute("DELETE FROM properties")

cursor.executemany("""
INSERT INTO properties
(title, location, price, bedrooms, bathrooms, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", properties)

connection.commit()
connection.close()

print("Properties added successfully!")