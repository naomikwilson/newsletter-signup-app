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

@app.route("/about")
def about():
    return render_template('about_us.html')

@app.route("/home")
def about():
    return render_template('homepage.html')

@app.route("/login")
def about():
    return render_template('Log_in.html')

@app.route("/matches")
def about():
    return render_template('matches.html')


if __name__ == "__main__":
    app.run(debug=True,port=5001)