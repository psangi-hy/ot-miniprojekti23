from flask import render_template, redirect, request

from app import app
import db_handling

@app.route("/", methods=["GET", "POST"])
def index():
    articles = list(db_handling.select_all_articles())
    books = list(db_handling.select_all_books())
    inproceedings = list(db_handling.select_all_inproceedings())
    return render_template(
        "index.html", articles=articles, books=books, inproceedings=inproceedings)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        reference_type = request.form.get("type")
        author = request.form.get("author")
        title = request.form.get("title")
        year = request.form.get("year")
        pages = request.form.get("pages")

        journal_or_publisher_or_booktitle = (request.form.get("journal")
            or request.form.get("publisher")
            or request.form.get("booktitle"))
        volume = request.form.get("volume")

        # Generate a key for the reference
        key = db_handling.bibtexgen(author, year, volume, pages)

        if reference_type == "article":
            if db_handling.new_article(
                key, author, title, journal_or_publisher_or_booktitle, year, volume, pages):
                return redirect("/")
        elif reference_type == "book":
            if db_handling.new_book(
                key, author, title, year, journal_or_publisher_or_booktitle, volume, pages):
                return redirect("/")
        elif reference_type == "inproceeding":
            if db_handling.new_inproceeding(
                key, author, title, year, journal_or_publisher_or_booktitle, pages):
                return redirect("/")

    return render_template("new.html")


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")
