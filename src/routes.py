from flask import render_template, redirect, request

from app import app
import db_handling

@app.route("/", methods=["GET", "POST"])
def index():
    articles = list(db_handling.select_all_articles())
    books = list(db_handling.select_all_books())
    inproceedings = list(db_handling.select_all_inproceedings())
    return render_template("index.html", items=articles, books=books, inproceedings=inproceedings)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    reference_type = request.form["type"]
    author = request.form["author"]
    year = request.form["year"]
    volume = request.form["volume"]
    title = request.form["title"]
    journal = request.form["journal"]
    pages = request.form["pages"]
    publisher = request.form["publisher"]
    booktitle = request.form["booktitle"]

    # Luo key käyttäen authorin isoja kirjaimia, julkaisu vuotta, painosta ja sivunumeroita
    key = db_handling.bibtexgen(author,year,volume,pages)

    if reference_type == "article" and db_handling.new_article(
            key, author, title, journal, year, volume, pages):
        return redirect("/")
    elif reference_type == "book" and db_handling.new_book(
            key, author, title, year, publisher, volume, pages):
        return redirect("/")
    elif reference_type == "inproceedings" and db_handling.new_inproceedings(
            key, author, title, year, booktitle, pages):
        return redirect("/")
    else:
        return render_template("error.html", message="Something went wrong...")


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")
