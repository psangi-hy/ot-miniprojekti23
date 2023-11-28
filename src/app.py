from flask import Flask
import os
import sqlalchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Check if in testing mode
is_testing = os.getenv('TESTING') == 'True'
# If testing, use test-database
database_name = 'test-database.sqlite' if is_testing else 'database.sqlite'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data', database_name)

from db import db
db.init_app(app)

def run_sql_schema():
    schema_path = os.path.join(basedir, 'schemas', 'schema.sql')

    with open(schema_path, 'r') as file:
        sql_schema = file.read()

    statements = sql_schema.split(';')

    with db.engine.connect() as connection:
        for statement in statements:
            if statement.strip():
                connection.execute(sqlalchemy.text(statement.strip() + ';'))

with app.app_context():
    # Check if the database file exists
    db_file_path = os.path.join('data', database_name)
    if not os.path.exists(db_file_path):
        db.create_all()  # Create database only if it doesn't exist

        # Run schema script
        try:
            run_sql_schema()
        except Exception as e:
            print(f"Error running schema: {e}")

import routes
