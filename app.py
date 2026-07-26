from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

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

if __name__ == '__main__':
    app.run(port=5555, debug=True)