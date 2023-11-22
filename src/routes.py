from app import app
import db_handling
from flask import render_template, redirect, request

@app.route("/", methods=["GET", "POST"])
def index():
    items = list(db_handling.database_test())
    return render_template("index.html", items=items)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    elif request.method == "POST":
        key = request.form("key")
        author = request.form("author")
        title = request.form("title")
        journal = request.form("journal")
        year = request.form("year")
        volume = request.form("volume")
        pages = request.form("pages")
        db_handling.new_article(key, author, title, journal, year, volume, pages)
        return redirect("/")
