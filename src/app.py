from flask import Flask
import os
import sqlalchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data/database.sqlite')

from db import db
db.init_app(app)

def run_sql_schema():
    schema_path = os.path.join(basedir, 'schemas', 'schema.sql')

    with open(schema_path, 'r') as file:
        sql_schema = file.read()

    with db.engine.connect() as connection:
        connection.execute(sqlalchemy.text(sql_schema))

with app.app_context():
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    db.create_all() # Create database
    # Create a better solution for this later
    try:
        run_sql_schema()
    except:
        pass

import routes
