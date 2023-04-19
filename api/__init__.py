from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1310526879@localhost:5432/mypass'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app
