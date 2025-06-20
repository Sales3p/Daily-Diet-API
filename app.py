from flask import Flask
from models.userMeal import db
from routes import bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///refeicoes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(bp)

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)