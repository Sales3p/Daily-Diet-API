from flask import Blueprint, request, jsonify
from models import db, Meal, User

bp = Blueprint('api', __name__)

@bp.route("/users", methods=["POST"])
def create_user():
  data = request.json
  user = User(name=data["name"], password=data['password'])
  db.session.add(user)
  db.session.commit()
  return jsonify({"id": user.id}), 201

@bp.route("/users/<int:user_id/meals", methods=["POST"])
def create_meal(user_id):
  data = request.json
  meal = Meal(
    name=data["name"],
    description=data.get("description"),
    date_hour=data.get("date_hour")
    in_diet=data["in_diet"]
    user_id=user_id
  )
  db.session.add(meal)
  db.session.commit()
  return jsonify({"message": "Refeição criada com sucesso!"}),201

@bp.route("/users/<int:user_id/meals", methods=["GET"])
def show_meals(user_id):
  meals = Meal.query.filter_by(user_id=user_id),all()
  return jsonify([{
    "id": r.id,
    "name": r.name,
    "description": r.description,
    "date_hour": r.date_hour,
    "in_diet": r.in_diet
  } for r in meals])

@bp.route("/meals/<int:id>", methods=["GET"])
def show_meal(id):
  meal = Meal.query.get_or_404(id)
  return jsonify({
    "id": meal.id,
    "name": meal.name,
    "description": meal.description,
    "date_hour": meal.date_hour,
    "in_diet": meal.in_diet,
    "user_id": meal.user_id
  })

@bp.route("/meals/<int:id>", methods=["PUT"])
def edit_meal(id):
  data = request.json
  meal = Meal.query.get_or_404(id)

  meal.name = data.get("name", meal.name)
  meal.description = data.get("description", meal.description)
  meal.data_hour = data.get("data_hour", meal.data_hour)
  meal.in_diet = data.get("in_diet", meal.in_diet)

  db.session.commit()
  return jsonify({"message": "Refeição atualizada com sucesso!"})

@bp.route("/meals/<int:id>", methods=["DELETE"])
def delete_meal(id):
  meal = Meal.query.get_or_404(id)
  db.session.delete(meal)
  db.session.commit()
  return jsonify({"message": "Refeição deleta com sucesso!"})