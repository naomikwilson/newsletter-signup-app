from flask import Flask, redirect, request, render_template, url_for
from historical_events import get_fact

app = Flask(__name__)


@app.route("/")
def historical_fact_post():
    year, fact = get_fact()
    return render_template("homepage.html", fact=fact, year=year)

"""
404 Handling
"""
@app.errorhandler(404)
def page_not_found(e):
    return "Not found. 😭"

@app.route("/about", endpoint = "about_page")
def about():
    return render_template('about_us.html')

@app.route("/home", endpoint = "home_page")
def about():
    return render_template('homepage.html')

@app.route("/login", endpoint = "log_in_page")
def about():
    return render_template('Log_in.html')

@app.route("/matches", endpoint = "matches_page")
def about():
    return render_template('matches.html')


if __name__ == "__main__":
    app.run(debug=True,port=5001)