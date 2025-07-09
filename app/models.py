from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.SmallInteger, nullable=False, default=0)
    profile_img = db.Column(db.String(100), nullable=True)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default= "Pending")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)