from app import app
import db_handling
from flask import render_template, redirect, session, request

@app.route("/", methods=["GET", "POST"])
def index():
    items = list(db_handling.database_test())
    return render_template("index.html", items=items)
