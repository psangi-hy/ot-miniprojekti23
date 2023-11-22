from db import db
from sqlalchemy.sql import text

def select_all_articles():
    sql = text("SELECT * FROM articles")
    result = db.session.execute(sql)
    return result

def new_article(key, author, title, journal, year, volume, pages):
    sql = text("INSERT INTO articles (key, author, title, journal, year, volume, pages) VALUES (:key, :author, :title, :journal, :year, :volume, :pages)")
    db.session.execute(sql, {"key": key, "author": author, "title": title, "journal": journal, "year": year, "volume": volume, "pages": pages})
    db.session.commit()
