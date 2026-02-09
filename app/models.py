from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    content = db.Column(db.Text)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(10))
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    input_format = db.Column(db.String(100))
    constraints = db.Column(db.String(100))
    output_format = db.Column(db.String(100))
    sample_input = db.Column(db.String(100))
    sample_output = db.Column(db.String(100))
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(100))
