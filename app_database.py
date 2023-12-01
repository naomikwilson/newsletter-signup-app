from flask import Flask, redirect, render_template, request, g
import sqlite3

app = Flask(__name__)


# 1. Configuration settings
app.config["TEMPLATES_AUTO_RELOAD"] = True
DATABASE = "newsletter.db"


# 2. Database initialization
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS newsletters (
            newsletter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            newsletter_name TEXT
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS newsletter_subscriptions (
            newsletter_subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            newsletter_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(newsletter_id) REFERENCES users(newsletter_id)
        )
    """
    )
    db.commit()


def get_db():
    if not hasattr(g, "db"):
        g.db = sqlite3.connect(DATABASE)
    return g.db


with app.app_context():
    create_table()

# 3. Request handling
@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


# #4. Route definitions
# @app.route("/") 
# def index(): 
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     return render_template("index.html", users=users)


# @app.post("/add")
# def add_user():
#     name = request.form.get("name")
#     email = request.form.get("email")
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO users (username, email) VALUES (?, ?);", (name, email))
#     db.commit()
#     return redirect("/")

"""
404 Handling
"""
@app.errorhandler(404)
def page_not_found(e):
    return "Not found. 😭"


if __name__ == "__main__":
    app.run(debug=True,port=5002)