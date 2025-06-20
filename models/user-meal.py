from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __dailyDiet__ = 'users'
  id = db.Colunm(db.Integer, primary_key=True)
  name = db.Colunm(db.String(80), unique=True nullable=False)
  password = db.Colunm(db.String(80), nullable=False)

  meals = db.relationship('Meal', backref='user', lazy=True)

class Meal(db.model):
  __dailyDiet__ = 'meals'
  id = db.Colunm(db.Integer, primary_key=True)
  name = db.Colunm(db.String(80), nullable=False)
  description = db.Colunm(db.Text)
  date_hour = db.Colunm(db.DateTime, default=datetime.utcnow)
  in_diet = db.Colunm(db.Boolean, default=True)

  user_id = db.Colunm(db.Integer, db.ForeignKey('users.id'), nullable=False)
