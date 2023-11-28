import os
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


def new_article(key, author, title, journal, year, volume, pages):
    if len(key) == 0 or len(author) == 0 or len(title) == 0  or len(journal) == 0 or len(year) == 0:
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
    if len(key)== 0 or len(author) == 0 or len(title) == 0 or len(publisher) == 0 or len(year) == 0:
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
    if len(author) == 0 or len(title) == 0 or len(booktitle) == 0 or len(year) == 0:
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

def bibtexgen(author,year,volume,pages):
    key = f"{''.join(word[0].upper() for word in author.split())}{year}{volume}{''.join(char for char in pages if char.isdigit())}"

    return key
