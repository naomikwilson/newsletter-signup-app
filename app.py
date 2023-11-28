from flask import Flask, redirect, request, render_template, url_for
from historical_events import get_fact

app = Flask(__name__)


@app.post("/")
def fun_fact_post():
    year, fact = get_fact()
    return render_template("page_to_put_it_on.html", fact=fact, year=year)
    # on page_to_put_it_on.html, we'd put something like:
    # <p> Historical fact: on this month and day in year {{ year }}, {{ fact }} </p>
