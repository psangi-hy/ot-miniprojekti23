from db import db
from sqlalchemy.sql import text

def database_test():
    sql = text("SELECT * FROM articles")
    result = db.session.execute(sql)
    return result
