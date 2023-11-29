from flask import render_template, redirect, request

from app import app
import db_handling

@app.route("/", methods=["GET", "POST"])
def index():
    articles = db_handling.select_all_articles()
    books = db_handling.select_all_books()
    inproceedings = db_handling.select_all_inproceedings()
    return render_template("index.html", articles=articles, books=books, inproceedings=inproceedings)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")

    reference_type = request.form.get("type", default="")
    author = request.form.get("author", default="")
    year = request.form.get("year", default="")
    volume = request.form.get("volume", default="")
    title = request.form.get("title", default="")
    journal = request.form.get("journal", default="")
    pages = request.form.get("pages", default="")
    publisher = request.form.get("publisher", default="")
    booktitle = request.form.get("booktitle", default="")

    # Luo key käyttäen authorin isoja kirjaimia, julkaisu vuotta, painosta ja sivunumeroita
    key = db_handling.bibtexgen(author,year,volume,pages)

    if reference_type == "article" and db_handling.new_article(
            key, author, title, journal, year, volume, pages):
        return redirect("/")

    if reference_type == "book" and db_handling.new_book(
            key, author, title, year, publisher, volume, pages):
        return redirect("/")

    if reference_type == "inproceeding" and db_handling.new_inproceeding(
            key, author, title, year, booktitle, pages):
        return redirect("/")

    return render_template("error.html", message="Something went wrong...")


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")
