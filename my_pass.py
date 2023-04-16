from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1310526879@localhost:5432/mypass_test'

db = SQLAlchemy(app)


class it_college(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    unique_code = db.Column(db.String(10), unique=True, nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey("it_college_type.id"), nullable=False, )
    type = db.relationship('it_college_type', backref='it_colleges')

    def __repr__(self):
        return f"<it_college:{self.id}>"


class it_college_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<it_college_type:{self.id}>"


if __name__ == "__main__":
    app.run(debug=True)
