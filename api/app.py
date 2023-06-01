from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__, template_folder='templates')
api = Api(app)

with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:pupelo35@localhost:5432/mypass'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

with app.app_context():
    db.create_all()
