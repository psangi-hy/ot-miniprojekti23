from flask import render_template, redirect, request, jsonify

from app import app
import db_handling


@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get(
        "search_query") if request.method == "POST" else None
    search_option = request.form.get("search_option", None)
    all_references = db_handling.get_all_references(search_query, search_option)
    return render_template("index.html",
                           references=all_references,
                           search_query=search_query,
                           search_option=search_option)


@app.route("/sort", methods=["GET"])
def sort():
    sort_by = request.args.get("sort_by", default="type")
    order = request.args.get("order", default="asc")

    all_references = db_handling.get_all_references()

    sorted_references = sorted(
        all_references, key=lambda x: x[sort_by], reverse=order == "desc")

    return jsonify(sorted_references)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")

    doi = request.form.get("doi", default="")
    if doi:
        doi_data = db_handling.fetch_by_doi(doi)
        if 'error' in doi_data:
            return render_template("error.html",
                                   message=f"Invalid DOI submitted ({doi_data['error']})")
        return render_template("new.html", form_data=doi_data)

    reference_type = request.form.get("type", default="")
    author = request.form.get("author", default="")
    year = request.form.get("year", default="")
    volume = request.form.get("volume", default="")
    title = request.form.get("title", default="")
    journal = request.form.get("journal", default="")
    pages = request.form.get("pages", default="")
    publisher = request.form.get("publisher", default="")
    booktitle = request.form.get("booktitle", default="")
    tag = request.form.get("tag", default="")

    key = db_handling.bibtexgen(author, year)

    if reference_type == "article" and db_handling.new_article(
            key, author, title, journal, year, volume, pages, tag):
        return redirect("/")

    if reference_type == "book" and db_handling.new_book(
            key, author, title, year, publisher, volume, pages, tag):
        return redirect("/")

    if reference_type == "inproceeding" and db_handling.new_inproceeding(
            key, author, title, year, booktitle, pages, tag):
        return redirect("/")
    
    if doi == "":
        return render_template("error.html", message="No DOI submitted. Please enter a DOI.")
    return render_template("error.html", message="Something went wrong...")


@app.route("/bibtex", methods=["GET", "POST"])
def bibtex():
    search_query = request.form.get(
        "search_query") if request.method == "POST" else None
    search_option = request.form.get("search_option", None)

    articles = db_handling.select_all_articles(search_query, search_option)
    books = db_handling.select_all_books(search_query, search_option)
    inproceedings = db_handling.select_all_inproceedings(search_query, search_option)

    return render_template("bibtex.html",
                           articles=articles,
                           books=books,
                           inproceedings=inproceedings,
                           search_query=search_query,
                           search_option=search_option)


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
