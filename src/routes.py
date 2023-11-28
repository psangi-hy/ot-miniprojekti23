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
    author = request.form["author"]
    year = request.form["year"]
    volume = request.form["volume"]
    title = request.form["title"]
    journal = request.form["journal"]
    pages = request.form["pages"]

    # Luo key käyttäen authorin isoja kirjaimia, julkaisu vuotta, painosta ja sivunumeroita
    key = f"{''.join(word[0].upper() for word in author.split())}{year}{volume}{''.join(char for char in pages if char.isdigit())}"

    if db_handling.new_article(key, author, title, journal, year, volume, pages):
        return redirect("/")
    return render_template("error.html", message="Something went wrong...")


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")
