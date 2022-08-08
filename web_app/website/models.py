# from website import db
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    textData = db.Column(db.String(10000))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))
    firstName = db.Column(db.String(150))
    moods = db.relationship('Mood')