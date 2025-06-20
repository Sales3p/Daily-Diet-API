from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)

  meals = db.relationship('Meal', backref='user', lazy=True, cascade="all, delete")

class Meal(db.Model):
  __tablename__ = 'meals'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.Text)
  date_hour = db.Column(db.DateTime, default=datetime.utcnow)
  in_diet = db.Column(db.Boolean, default=True)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
