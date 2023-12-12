# Reference: flask-app-demo repository by lzblack / Zhi Li on GitHub
# Debugged using ChatGPT (per professor's suggestion)

from flask import Flask, redirect, render_template, request, g, flash
import sqlite3
from historical_events import get_fact
from password_verification import password_verification, hash_password
from newsletter_suggestions import get_newsletter_suggestions, get_all_newsletter_names
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


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
            newsletter_name TEXT UNIQUE -- Add UNIQUE constraint to prevent duplicates
        )
    """
    )

    all_newsletter_names = get_all_newsletter_names()
    for newsletter in all_newsletter_names:
        # Check if the newsletter already exists
        cursor.execute(
            "SELECT newsletter_name FROM newsletters WHERE newsletter_name = ?;",
            (newsletter,),
        )
        existing_newsletter = cursor.fetchone()

        if not existing_newsletter:
            cursor.execute(
                "INSERT INTO newsletters (newsletter_name) VALUES (?);", (newsletter,)
            )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS newsletter_subscriptions (
            newsletter_subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            newsletter_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(newsletter_id) REFERENCES newsletters(newsletter_id)
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


current_user = ""
suggestions = ""


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


@app.get("/login", endpoint="log_in_page_get")
def log_in_get():
    return render_template("Log_in.html")


@app.route("/login", methods=["POST"], endpoint="log_in_page_post")
def log_in_post():
    # get data from database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username, hashed_password FROM users")
    users = dict(cursor.fetchall())

    # validate the input
    user = request.form.get("username")
    password = request.form.get("password")

    if user not in users:
        flash(
            "User not found; please create an account by clicking the button above",
            "error",
        )
        return render_template("Log_in.html")

    hashed_password = users.get(user)
    # if the password is correct (hashed version matches one in database)
    if password_verification(password, hashed_password):
        # set user to current_user to indicate the user has logged in
        global current_user
        current_user = user
        return redirect("/matches")
    else:
        flash("Incorrect password", "error")
        return render_template("Log_in.html")


@app.get("/create-new", endpoint="create_new_account_page_get")
def create_new_account_post():
    return render_template("create_an_account.html")


@app.route("/create-new", methods=["POST"], endpoint="create_new_account_page_post")
def create_new_account_post():
    new_user = request.form.get("username")
    new_password = request.form.get("password-input")
    new_hashed_password = hash_password(new_password)

    db = get_db()
    cursor = db.cursor()
    # select two fields to be able to turn rows into dict
    cursor.execute("SELECT username, user_id FROM users")
    rows = cursor.fetchall()

    if rows:
        users = dict(rows)
    else:
        users = {}

    if new_user not in users:  # confirm that username is not already taken
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?);",
            (new_user, new_hashed_password),
        )
        db.commit()
        flash("User created successfully", "success")
        # set user to current_user to indicate the user has logged in
        global current_user
        current_user = new_user
        return redirect("/matches")
    else:
        flash("Username is already taken. Please enter another username", "error")
        return render_template("create_an_account.html")


@app.get("/matches", endpoint="matches_page_get")
def matches_get():
    return render_template("matches.html")


@app.route("/matches", methods=["POST"], endpoint="matches_page_post")
def matches_post():
    selected_categories = request.form.getlist("option")

    # Get suggested newsletters (dictionary with name:link pairs)
    global suggestions # Keep track of suggestions (to be used for dashboard)
    suggestions = get_newsletter_suggestions(selected_categories)

    return redirect("/dashboard")


@app.get("/dashboard", endpoint="dashboard_get")
def results_get():
    db = get_db()
    cursor = db.cursor()
    global current_user
    cursor.execute("SELECT user_id FROM users WHERE username = ?;", (current_user,))
    user_id = cursor.fetchone()[0] # Access the first (and only) element in the tuple

    # Get newsletters saved by user
    cursor.execute(
        "SELECT newsletter_name FROM newsletters INNER JOIN newsletter_subscriptions ON newsletters.newsletter_id = newsletter_subscriptions.newsletter_id WHERE user_id = ?;",
        (user_id,),
    )
    saved_newsletters_tuples_list = cursor.fetchall()

    # Transform from a list of tuples to a list
    saved_newsletters_list = []
    for newsletter in saved_newsletters_tuples_list:
        saved_newsletters_list.append(newsletter[0])

    # Newsletter suggestions generated from matches page
    global suggestions
    return render_template(
        "dashboard.html",
        username=current_user,
        saved_newsletters=saved_newsletters_list,
        suggestions=suggestions,
    )


@app.route("/dashboard", methods=["POST"], endpoint="dashboard_post")
def results_post():
    # Get newsletters to add to database for user
    newsletters_to_add = request.form.getlist("add")
    # Get newsletters to delete from database for user
    newsletters_to_delete = request.form.getlist("delete")  

    db = get_db()
    cursor = db.cursor()
    global current_user
    cursor.execute("SELECT user_id FROM users WHERE username = ?;", (current_user,))
    user_id = cursor.fetchone()[0] # Access the first (and only) element in the tuple

    # If there are newsletters that need to be added to the newsletter_subscription table
    if newsletters_to_add:
        for newsletter in newsletters_to_add:
            # get newsletter id of newsletter to add
            cursor.execute(
                "SELECT newsletter_id FROM newsletters WHERE newsletter_name = ?;",
                (newsletter,),
            )
            newsletter_id = cursor.fetchone()[0]

            # add user id and newsletter id to database to save suggested newsletter
            cursor.execute(
                "INSERT INTO newsletter_subscriptions (user_id, newsletter_id) VALUES (?, ?);",
                (user_id, newsletter_id),
            )
            db.commit()
            flash("Newsletters successfully added to list", "success")

    # If there are newsletters that need to be removed from the newsletter_subscription table
    if newsletters_to_delete:
        for newsletter in newsletters_to_delete:
            # get newsletter id of newsletter to add
            cursor.execute(
                "SELECT newsletter_id FROM newsletters WHERE newsletter_name = ?;",
                (newsletter,),
            )
            newsletter_id = cursor.fetchone()[0]

            # delete entry with the corresponding newsletter id and user id
            cursor.execute(
                    "DELETE FROM newsletter_subscriptions WHERE user_id = ? AND newsletter_id = ?;",
                (user_id, newsletter_id),
            )
            db.commit()
            flash("Newsletters successfully deleted from list", "success")

    return redirect("/dashboard")


"""
404 Handling
"""


@app.errorhandler(404)
def page_not_found(e):
    return "Not found. 😭"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
