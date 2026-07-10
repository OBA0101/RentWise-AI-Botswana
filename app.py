from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# ==========================================
# Database Connection
# ==========================================
def get_db_connection():
    connection = sqlite3.connect("rentwise.db")
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# Home Page
# ==========================================
@app.route("/")
def home():

    search = request.args.get("search")

    connection = get_db_connection()
    cursor = connection.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM properties WHERE location LIKE ?",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM properties")

    properties = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        properties=properties,
        search=search
    )


# ==========================================
# Property Details
# ==========================================
@app.route("/property/<int:id>")
def property_details(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=?",
        (id,)
    )

    property = cursor.fetchone()

    connection.close()

    if property is None:
        return "Property not found", 404

    return render_template(
        "property.html",
        property=property
    )


# ==========================================
# Book Viewing
# ==========================================
@app.route("/book/<int:id>", methods=["GET", "POST"])
def book_property(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=?",
        (id,)
    )

    property = cursor.fetchone()

    if property is None:
        connection.close()
        return "Property not found", 404

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        viewing_date = request.form["date"]

        cursor.execute(
            """
            INSERT INTO bookings
            (property_id, fullname, email, phone, viewing_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                id,
                fullname,
                email,
                phone,
                viewing_date
            )
        )

        connection.commit()
        connection.close()

        return render_template(
            "success.html",
            fullname=fullname,
            email=email,
            property=property
        )

    connection.close()

    return render_template(
        "booking.html",
        property=property
    )


# ==========================================
# Dashboard
# ==========================================
@app.route("/dashboard")
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM properties")
    total_properties = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            bookings.*,
            properties.title
        FROM bookings
        JOIN properties
        ON bookings.property_id = properties.id
        ORDER BY bookings.id DESC
    """)

    bookings = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        total_properties=total_properties,
        total_bookings=total_bookings,
        bookings=bookings
    )


# ==========================================
# Add Property
# ==========================================
@app.route("/add-property", methods=["GET", "POST"])
def add_property():

    if request.method == "POST":

        title = request.form["title"]
        location = request.form["location"]
        price = request.form["price"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        description = request.form["description"]
        image = request.form["image"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO properties
            (title, location, price, bedrooms, bathrooms, description, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            location,
            price,
            bedrooms,
            bathrooms,
            description,
            image
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("dashboard"))

    return render_template("add_property.html")


# ==========================================
# Run Flask
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)