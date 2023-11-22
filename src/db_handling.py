from sqlalchemy.sql import text
from app import run_sql_schema
from db import db
import os

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

def reset_tests():
    os.remove("data/database.sqlite")
    f = open("data/database.sqlite", "x")
    f.close()
    run_sql_schema()
