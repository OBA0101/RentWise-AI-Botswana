from flask import Flask, render_template, request
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
# Run Flask
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)


# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)