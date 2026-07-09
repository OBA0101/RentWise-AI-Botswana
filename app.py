from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("rentwise.db")
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------
# Home Page
# -----------------------------
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


# -----------------------------
# Property Details Page
# -----------------------------
@app.route("/property/<int:id>")
def property_details(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id = ?",
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


if __name__ == "__main__":
    app.run(debug=True)