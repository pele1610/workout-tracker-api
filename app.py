from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from datetime import date

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    result = []
    for workout in workouts:
        result.append({
            "id": workout.id,
            "date": str(workout.date),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        })
    return jsonify(result), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get(id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    exercises_list = []
    for exercise in workout.exercises:
        exercises_list.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category
        })

    result = {
        "id": workout.id,
        "date": str(workout.date),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises_list
    }
    return jsonify(result), 200
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        new_workout = Workout(
            date=date.fromisoformat(data.get("date")),
            duration_minutes=data.get("duration_minutes"),
            notes=data.get("notes")
        )
        db.session.add(new_workout)
        db.session.commit()
    except (ValueError, TypeError) as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": new_workout.id,
        "date": str(new_workout.date),
        "duration_minutes": new_workout.duration_minutes,
        "notes": new_workout.notes
    }), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    for we in workout.workout_exercises:
        db.session.delete(we)

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": f"Workout {id} deleted"}), 200

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    result = []
    for exercise in exercises:
        result.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        })
    return jsonify(result), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    workouts_list = []
    for workout in exercise.workouts:
        workouts_list.append({
            "id": workout.id,
            "date": str(workout.date)
        })

    result = {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": workouts_list
    }
    return jsonify(result), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        new_exercise = Exercise(
            name=data.get("name"),
            category=data.get("category"),
            equipment_needed=data.get("equipment_needed", False)
        )
        db.session.add(new_exercise)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": new_exercise.id,
        "name": new_exercise.name,
        "category": new_exercise.category,
        "equipment_needed": new_exercise.equipment_needed
    }), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    for we in exercise.workout_exercises:
        db.session.delete(we)

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": f"Exercise {id} deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)