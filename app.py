# Reference: flask-app-demo repository by lzblack / Zhi Li on GitHub

from flask import Flask, redirect, render_template, request, g
import sqlite3
from historical_events import get_fact
from password_verification import password_verification, hash_password
from newsletter_suggestions import get_newsletter_suggestions

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
            username TEXT NOT NULL,
            hashed_password TEXT NOT NULL
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

current_user = ""


@app.route("/")
def historical_fact_post():
    year, fact = get_fact()
    return render_template("homepage.html", fact=fact, year=year)


@app.route("/about", endpoint="about_page")
def about():
    return render_template("about_us.html")


@app.route("/home", endpoint="home_page")
def home():
    return render_template("homepage.html")


@app.get("/login", endpoint="log_in_page")
def log_in_get():
    return render_template("Log_in.html")


@app.post("/login", endpoint="log_in_page")
def log_in_post():
    # get data from database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    # validate the input
    user = request.form.get("username")
    password = request.form.get("password")
    if user not in users:
        print("User not found; please create an account by clicking the button above")
    else:
        cursor.execute("SELECT hashed_password FROM users WHERE username = (?);"(user))
        hashed_password = cursor.fetchall()
        if password_verification(password, hashed_password):
            # add user to current_user dict to indicate the user has logged in
            current_user = user
            return redirect("/matches")


@app.get("/create-new", endppoint="create_new_account_page")
def create_new_account_post():
    return render_template("create_an_account.html")


@app.post("/create-new", endppoint="create_new_account_page")
def create_new_account_post():
    new_user = request.form.get("username")
    new_password = request.form.get("password-input")
    new_hashed_password = hash_password(new_password)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    if new_user not in users:  # confirm that username is not already taken
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?);",
            (new_user, new_hashed_password),
        )
        current_user = new_user
        return redirect("/matches")
    else:
        print("Username is already taken. Please enter another username")


@app.get("/matches", endpoint = "matches_page")
def matches_get():
    return render_template("matches.html")

@app.post("/matches", endpoint = "matches_page")
def matches_post():
    selected_categories = ""
    suggestions = get_newsletter_suggestions(selected_categories)











"""
404 Handling
"""


@app.errorhandler(404)
def page_not_found(e):
    return "Not found. 😭"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
