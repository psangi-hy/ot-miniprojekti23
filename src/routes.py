from flask import render_template, redirect, request

from app import app
import db_handling

@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get("search_query")
 
    articles = db_handling.select_all_articles(search_query)
    books = db_handling.select_all_books(search_query)
    inproceedings = db_handling.select_all_inproceedings(search_query)

    all_references = []

    for article in articles:
        article_dict = article._asdict()
        article_dict['type'] = 'article'
        all_references.append(article_dict)

    for book in books:
        book_dict = book._asdict()
        book_dict['type'] = 'book'
        all_references.append(book_dict)

    for inproceeding in inproceedings:
        inproceeding_dict = inproceeding._asdict()
        inproceeding_dict['type'] = 'inproceeding'
        all_references.append(inproceeding_dict)

    return render_template("index.html", references=all_references)


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

    key = db_handling.bibtexgen(author,year)

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


@app.route("/bibtex", methods=["GET", "POST"])
def bibtex():
    search_query = request.form.get("search_query")

    articles = db_handling.select_all_articles(search_query)
    books = db_handling.select_all_books(search_query)
    inproceedings = db_handling.select_all_inproceedings(search_query)

    return render_template("bibtex.html",
                            articles=articles,
                            books=books,
                            inproceedings=inproceedings)


@app.route("/reference/<ref_type>/<int:ref_id>")
def reference_item(ref_type, ref_id):
    select_func = {
        "article": db_handling.article_by_id,
        "book": db_handling.book_by_id,
        "inproceeding": db_handling.inproceeding_by_id,
    }.get(ref_type)

    if not select_func:
        return render_template("error.html", message="The page was not found."), 404

    reference = select_func(ref_id)

    if not reference:
        return render_template("error.html", message="The page was not found."), 404

    return render_template("reference.html", reftype=ref_type, reference=reference)


@app.route("/tests/reset", methods=["GET", "POST"])
def tests_reset():
    db_handling.reset_tests()
    return redirect("/")


@app.route("/reference/<ref_type>/<int:ref_id>/delete", methods=["POST"])
def delete(ref_type, ref_id):
    db_handling.delete_reference(ref_type, ref_id)
    return redirect("/")
