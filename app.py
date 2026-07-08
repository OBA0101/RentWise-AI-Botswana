from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Home Page
@app.route("/")
def home():

    search = request.args.get("search")

    connection = sqlite3.connect("rentwise.db")
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


# Property Details Page
@app.route("/property/<int:id>")
def property_details(id):

    connection = sqlite3.connect("rentwise.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=?",
        (id,)
    )

    property = cursor.fetchone()

    connection.close()

    return render_template(
        "property.html",
        property=property
    )


if __name__ == "__main__":
    app.run(debug=True)