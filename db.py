from flask_sqlalchemy import SQLAlchemy
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "database/database.sqlite"
db = SQLAlchemy(app)
