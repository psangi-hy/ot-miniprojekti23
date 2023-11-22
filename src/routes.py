from flask import render_template, redirect, request

from app import app
import db_handling

@app.route("/", methods=["GET", "POST"])
def index():
    items = list(db_handling.select_all_articles())
    return render_template("index.html", items=items)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    key = request.form["key"]
    author = request.form["author"]
    title = request.form["title"]
    journal = request.form["journal"]
    year = request.form["year"]
    volume = request.form["volume"]
    pages = request.form["pages"]
    if db_handling.new_article(key, author, title, journal, year, volume, pages):
        return redirect("/")
    return render_template("error.html", message="Something went wrong...")


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")
