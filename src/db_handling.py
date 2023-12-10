from sqlalchemy.sql import text
from app import run_sql_schema
from db import db

def select_all(table, search_query=None):
    if search_query:
        sql = text(f"SELECT * FROM {table} "
            "WHERE author LIKE :query OR "
            "title LIKE :query OR "
            "year LIKE :query")

        result = db.session.execute(sql, {"query": f"%{search_query}%"})
    else:
        sql = text(f"SELECT * FROM {table}")
        result = db.session.execute(sql)
    return result.all()


def select_all_articles(search_query=None):
    return select_all("articles", search_query)


def select_all_books(search_query=None):
    return select_all("books", search_query)


def select_all_inproceedings(search_query=None):
    return select_all("inproceedings",search_query)


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

def new_article(key, author, title, journal, year, volume, pages):
    if not key or not author or not title or not journal or year is None \
    or any(len(value) > 100 for value in (key, author, title, journal)):
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO articles (key, author, title, journal, year, volume, pages)"
            "VALUES (:key, :author, :title, :journal, :year, :volume, :pages)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "journal": journal,
                             "year": year,
                             "volume": volume,
                             "pages": pages})
    db.session.commit()
    return True


def new_book(key, author, title, year, publisher, volume, pages):
    if not key or not author or not title or not publisher or year is None \
    or any(len(value) > 100 for value in (key, author, title, publisher)):
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO books (key, author, title, year, publisher, volume, pages)"
            "VALUES (:key, :author, :title, :year, :publisher, :volume, :pages)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "year": year,
                             "publisher": publisher,
                             "volume": volume,
                             "pages": pages})
    db.session.commit()
    return True


def new_inproceeding(key, author, title, year, booktitle, pages):
    if not key or not author or not title or not booktitle or year is None \
    or any(len(value) > 100 for value in (key, author, title, booktitle)):
        return False
    if not validate_year(year) or not validate_pages(pages):
        return False
    sql = text(
            "INSERT INTO inproceedings (key, author, title, year, booktitle, pages)"
            "VALUES (:key, :author, :title, :year, :booktitle, :pages)")
    db.session.execute(sql, {"key": key,
                             "author": author,
                             "title": title,
                             "year": year,
                             "booktitle": booktitle,
                             "pages": pages})
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
