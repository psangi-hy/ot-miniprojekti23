import os
from sqlalchemy.sql import text
from app import run_sql_schema
from db import db

def select_all_articles():
    sql = text("SELECT * FROM articles")
    result = db.session.execute(sql)
    return result
def select_all_books():
    sql = text("SELECT * FROM books")
    result = db.session.execute(sql)
    return result
def select_all_inproceedings():
    sql = text("SELECT * FROM inproceedings")
    result = db.session.execute(sql)
    return result

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

def new_inproceedings(key, author, title, year, booktitle, pages):
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
    sql = text(
        "DROP TABLE IF EXISTS articles;"
    )
    db.session.execute(sql)
    db.session.commit()

def reset_tests():
    drop_tables()
    run_sql_schema()
