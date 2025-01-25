from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(50))
    category = db.Column(db.String(50))
    # counts = db.Column(db.Integer)
    description = db.Column(db.String(200))
