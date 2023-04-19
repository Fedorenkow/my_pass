from datetime import datetime
from api import db


class it_college(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    unique_code = db.Column(db.String(10), unique=True, nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey("it_college_type.py.id"), nullable=False, )
    type = db.relationship('it_college_type.py', backref='it_colleges')

    def __repr__(self):
        return f"<it_college:{self.id}>"
