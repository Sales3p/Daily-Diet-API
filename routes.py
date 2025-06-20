from flask import Blueprint, request, jsonify
from models.userMeal import db, Meal, User
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route("/users", methods=["POST"])
def create_user():
  data = request.json
  user = User(name=data["name"], password=data['password'])
  db.session.add(user)
  db.session.commit()
  return jsonify({"id": user.id}), 201

@bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({"message": "Usuario deletado com sucesso!"})

@bp.route("/users/<int:user_id>/meals", methods=["POST"])
def create_meal(user_id):
  data = request.json

  date_str = data.get("date_hour")
  if date_str:
    date_hour = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
  else:
    date_hour = datetime.utcnow()

  in_diet_str = data.get("in_diet")
  if isinstance(in_diet_str, str):
    in_diet = in_diet_str.strip().lower() == "sim"
  else:
    in_diet = bool(in_diet_str)

  meal = Meal(
    name=data["name"],
    description=data.get("description"),
    date_hour=date_hour,
    in_diet=in_diet,
    user_id=user_id
  )
  db.session.add(meal)
  db.session.commit()
  return jsonify({"message": "Refeição criada com sucesso!"}),201

@bp.route("/users/<int:user_id>/meals", methods=["GET"])
def show_meals(user_id):
  meals = Meal.query.filter_by(user_id=user_id).all()
  return jsonify([{
    "id": r.id,
    "name": r.name,
    "description": r.description,
    "date_hour": r.date_hour,
    "in_diet": "Sim" if r.in_diet else "Não"
  } for r in meals])

@bp.route("/meals/<int:id>", methods=["GET"])
def show_meal(id):
  meal = Meal.query.get_or_404(id)
  return jsonify({
    "id": meal.id,
    "name": meal.name,
    "description": meal.description,
    "date_hour": meal.date_hour,
    "in_diet": "Sim" if meal.in_diet else "Não",
    "user_id": meal.user_id
  })

@bp.route("/meals/<int:id>", methods=["PUT"])
def edit_meal(id):
  data = request.json
  meal = Meal.query.get_or_404(id)

  meal.name = data.get("name", meal.name)
  meal.description = data.get("description", meal.description)
  
  date_str = data.get("date_hour")
  if date_str:
    date_hour = datetime.strptime(date_str, "%d/%m/%Y %H:%M")

  in_diet_raw = data.get("in_diet")
  if in_diet_raw is not None:
    if isinstance(in_diet_raw, str):
      meal.in_diet = in_diet_raw.strip().lower() == "sim"
    else:
      meal.in_diet = bool(in_diet_raw)

  db.session.commit()
  return jsonify({"message": "Refeição atualizada com sucesso!"})

@bp.route("/meals/<int:id>", methods=["DELETE"])
def delete_meal(id):
  meal = Meal.query.get_or_404(id)
  db.session.delete(meal)
  db.session.commit()
  return jsonify({"message": "Refeição deleta com sucesso!"})