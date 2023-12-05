from sqlalchemy.sql import text
from app import run_sql_schema
from db import db

def select_all(table):
    sql = text(f"SELECT * FROM {table}")
    result = db.session.execute(sql)
    return result.all()


def select_all_articles():
    return select_all("articles")


def select_all_books():
    return select_all("books")


def select_all_inproceedings():
    return select_all("inproceedings")


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


def validate_volume(volume):
    if len(volume) == 0:
        return True
    return validate_as_numbers(volume)


def new_article(key, author, title, journal, year, volume, pages):
    if len(key) == 0 or len(author) == 0 or len(title) == 0  or len(journal) == 0 or year is None:
        return False
    if not validate_year(year) or not validate_pages(pages) or not validate_volume(volume):
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
    if len(key)== 0 or len(author) == 0 or len(title) == 0 or len(publisher) == 0 or year is None:
        return False
    if not validate_year(year) or not validate_pages(pages) or not validate_volume(volume):
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
    if len(author) == 0 or len(title) == 0 or len(booktitle) == 0 or year is None:
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
        sql = text("DELETE FROM books WHERE id = :source_id")
        db.session.execute(sql, {"id": source_id})
    elif source_type == "article":
        sql = text("DELETE FROM articles WHERE id = :id")
        db.session.execute(sql, {"id": source_id})
    elif source_type == "inproceeding":
        sql = text("DELETE FROM inproceedings WHERE id = :id")
        db.session.execute(sql, {"id": source_id})


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


def bibtexgen(author,year,volume = None, pages = None):
    if volume is None or volume == "":
        volume = "0"
    if pages is None or pages == "":
        pages = "0"
    initials = ''.join(word[0].upper() for word in author.split())
    pages = ''.join(char for char in pages if char.isdigit())
    key = f"{initials}{year}{volume}{pages}"
    return key
