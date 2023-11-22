import os
from flask_sqlalchemy import SQLAlchemy
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))
if app.testing:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(
            basedir, 'data/test_database.sqlite')
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(
            basedir, 'data/database.sqlite')
db = SQLAlchemy(app)
