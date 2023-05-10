from datetime import datetime
from api.app import db


class it_college_type(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(30), nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<it_college:{self.id}>"
