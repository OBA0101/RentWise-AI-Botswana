import sqlite3

connection = sqlite3.connect("rentwise.db")
cursor = connection.cursor()

# Delete old data
cursor.execute("DELETE FROM properties")

# Property 1
cursor.execute("""
INSERT INTO properties
(title, location, price, bedrooms, bathrooms, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "Modern Apartment",
    "Gaborone",
    4500,
    2,
    1,
    "Beautiful apartment close to the city centre.",
    "/static/images/apartment1.jpg"
))

# Property 2
cursor.execute("""
INSERT INTO properties
(title, location, price, bedrooms, bathrooms, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "Family House",
    "Francistown",
    6800,
    3,
    2,
    "Perfect family home with a spacious yard.",
    "/static/images/apartment2.jpg"
))

# Property 3
cursor.execute("""
INSERT INTO properties
(title, location, price, bedrooms, bathrooms, description, image)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "Luxury Villa",
    "Maun",
    12000,
    5,
    4,
    "Luxury villa with swimming pool.",
    "/static/images/apartment3.jpg"
))

connection.commit()
connection.close()

print("Properties inserted successfully!")