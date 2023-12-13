import json
import requests
from sqlalchemy.sql import text
from app import run_sql_schema
from db import db

def get_all_references(search_query=None, search_option = None):
    articles = select_all_articles(search_query, search_option)
    books = select_all_books(search_query, search_option)
    inproceedings = select_all_inproceedings(search_query, search_option)

    all_references = []

    all_references.extend(
        __get_converted_db_data_list('article', articles))
    all_references.extend(
        __get_converted_db_data_list('book', books))
    all_references.extend(
        __get_converted_db_data_list('inproceeding', inproceedings))

    return all_references

def __get_converted_db_data_list(type_name: str, references):
    reference_list = []
    for reference in references:
        reference_dict = reference._asdict()
        reference_dict['type'] = type_name
        reference_list.append(reference_dict)
    return reference_list


def select_all(table, search_query=None, search_option=None):
    if search_query:
        search_terms = search_query.split()
        if search_option == "OR":
            conditions = " OR ".join([
                f"({table}.author LIKE :term{i}) OR "
                f"({table}.title LIKE :term{i}) OR "
                f"({table}.year LIKE :term{i}) OR "
                f"({table}.tag LIKE :term{i})"
                for i in range(len(search_terms))
            ])
        elif search_option == "AND":
            conditions = " AND ".join([
                f"({table}.author LIKE :term{i}) AND "
                f"({table}.title LIKE :term{i}) AND "
                f"({table}.year LIKE :term{i}) AND "
                f"({table}.tag LIKE :term{i})"
                for i in range(len(search_terms))
            ])

        sql = text(f"SELECT * FROM {table} WHERE {conditions}")
        params = {f"term{i}": f"%{term}%" for i, term in enumerate(search_terms)}
        result = db.session.execute(sql, params)

        return result.all()

    sql = text(f"SELECT * FROM {table}")
    result = db.session.execute(sql)
    return result.all()


def select_all_articles(search_query=None, search_option = None):
    return select_all("articles", search_query, search_option)


def select_all_books(search_query=None, search_option = None):
    return select_all("books", search_query, search_option)


def select_all_inproceedings(search_query=None, search_option = None):
    return select_all("inproceedings",search_query, search_option)


def by_id(table, item_id):
    sql = text(f"SELECT * FROM {table} WHERE id=:id")
    result = db.session.execute(sql, { "id": item_id })
    return result.one_or_none()


def article_by_id(article_id):
    return by_id("articles", article_id)


def book_by_id(book_id):
    return by_id("books", book_id)


def inproceeding_by_id(inproceeding_id):
    return by_id("inproceedings", inproceeding_id)


def validate_as_numbers(numbers):
    try:
        numbers = int(numbers)
        return True
    except ValueError:
        return False


def validate_year(year):
    return validate_as_numbers(year)


def validate_pages(pages):
    if len(pages) == 0:
        return True
    pages = pages.replace("-", "").replace(" ", "")
    return validate_as_numbers(pages)

def new_article(key, author, title, journal, year, volume, pages, tag):
    if len(key) == 0 or len(author) == 0 or len(title) == 0  or len(journal) == 0 or year is None:
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO articles (key, author, title, journal, year, volume, pages, tag)"
            "VALUES (:key, :author, :title, :journal, :year, :volume, :pages, :tag)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "journal": journal,
                             "year": year,
                             "volume": volume,
                             "pages": pages,
                             "tag":tag})
    db.session.commit()
    return True


def new_book(key, author, title, year, publisher, volume, pages, tag):
    if len(key)== 0 or len(author) == 0 or len(title) == 0 or len(publisher) == 0 or year is None:
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO books (key, author, title, year, publisher, volume, pages,tag)"
            "VALUES (:key, :author, :title, :year, :publisher, :volume, :pages, :tag)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "year": year,
                             "publisher": publisher,
                             "volume": volume,
                             "pages": pages,
                             "tag": tag})
    db.session.commit()
    return True


def new_inproceeding(key, author, title, year, booktitle, pages, tag):
    if len(author) == 0 or len(title) == 0 or len(booktitle) == 0 or year is None:
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO inproceedings (key, author, title, year, booktitle, pages, tag)"
            "VALUES (:key, :author, :title, :year, :booktitle, :pages, :tag)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "year": year,
                             "booktitle": booktitle,
                             "pages": pages,
                             "tag": tag})
    db.session.commit()
    return True


def delete_reference(source_type, source_id):
    if source_type == "book":
        sql = text("DELETE FROM books WHERE id = :id")
    elif source_type == "article":
        sql = text("DELETE FROM articles WHERE id = :id")
    elif source_type == "inproceeding":
        sql = text("DELETE FROM inproceedings WHERE id = :id")
    db.session.execute(sql, {"id": source_id})
    db.session.commit()
    return True

def drop_tables():
    sql_statements = [text("DROP TABLE IF EXISTS articles;"),
        text("DROP TABLE IF EXISTS books;"),
        text("DROP TABLE IF EXISTS inproceedings;")]

    for statement in sql_statements:
        db.session.execute(statement)

    db.session.commit()


def reset_tests():
    drop_tables()
    run_sql_schema()


def bibtexgen(author,year):
    initials = ''.join(word[0].upper() for word in author.split() if word[0].isalpha())[:2]
    key = f"{initials}{year}"

    count = 0
    while True:

        suffix = chr(ord('A') + count)

        sql = text("""
        SELECT COUNT(*) FROM articles WHERE key=:key
        UNION ALL
        SELECT COUNT(*) FROM books WHERE key=:key
        UNION ALL
        SELECT COUNT(*) FROM inproceedings WHERE key=:key
        """)

        result = db.session.execute(sql, {"key": key}).fetchall()

        if all(row[0] == 0 for row in result):
            break

        key = f"{initials}{year}{suffix}"
        count += 1

    return key

def article_data(dict1, source, keys):
    dict1["type"] = "article"
    try:
        dict1["journal"] = source["container-title"]
    except KeyError:
        dict1["journal"] = ""

    if "volume" in keys:
        dict1["volume"] = source["volume"]
    if "page" in keys:
        dict1["pages"] = source["page"]

def proceedings_data(dict1, source):
    dict1["type"] = "inproceeding"
    try:
        dict1["booktitle"] = source["container-title"]
    except KeyError:
        dict1["booktitle"] = ""

def book_data(dict1, source, keys):
    dict1["type"] = "book"
    try:
        dict1["publisher"] = source["publisher"]
    except KeyError:
        dict1["publisher"] = ""

    if "volume" in keys:
        dict1["volume"] = source["volume"]
    if "page" in keys:
        dict1["pages"] = source["page"]

def source_data(dict1, source, keys):
    try:
        author = f"{source['author'][0]['family']}, {source['author'][0]['given']}"
        if len(source["author"])>1:
            author += f" and {source['author'][1]['family']}, {source['author'][1]['given']}"
        dict1["author"] = author
    except KeyError:
        dict1["author"] = ""

    try:
        dict1["title"] = f"{source['title']}"
        if "subtitle" in keys and source["subtitle"]:
            dict1["title"] += f": {source['subtitle'][0]}"
    except KeyError:
        dict1["title"] = ""

    try:
        dict1["year"] = source["published"]["date-parts"][0][0]
    except KeyError:
        dict1["year"] = ""

def fetch_by_doi(doi):
    url = "https://dx.doi.org/" + str(doi)
    header = {'accept': 'application/citeproc+json'}
    result = requests.get(url, headers=header, timeout=6)

    data = None
    try:
        data = result.json()
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON response'}

    if result.status_code == 200:
        data = json.loads(result.text)
    if result.status_code != 200:
        return {'error': f'HTTP Error: {result.status_code}'}
    keys = data.keys()
    formatted = {}

    source_data(formatted, data, keys)

    if data["type"] == "journal-article":
        article_data(formatted, data, keys)

    elif data["type"] == "proceedings-article":
        proceedings_data(formatted, data)

    elif data["type"] == "book-chapter":
        book_data(formatted, data, keys)

    return formatted
