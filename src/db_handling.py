import os
from sqlalchemy.sql import text
from app import run_sql_schema
from db import db

def select_all_articles():
    sql = text("SELECT * FROM articles")
    result = db.session.execute(sql)
    return result

def new_article(key, author, title, journal, year, volume, pages):
    if len(key)== 0 or len(author) == 0 or len(year) == 0 or len(journal) == 0 or len(title) == 0:
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

def drop_tables():
    sql = text(
        "DROP TABLE IF EXISTS articles;"
    )
    db.session.execute(sql)
    db.session.commit()

def reset_tests():
    drop_tables()
    run_sql_schema()
