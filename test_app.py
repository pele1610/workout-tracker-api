import pytest
from app import app
from models import db, Exercise, Workout, WorkoutExercise


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()
        db.drop_all()


def test_exercise_name_validation(client):
    with app.app_context():
        with pytest.raises(ValueError):
            Exercise(name="", category="strength")


def test_exercise_category_validation(client):
    with app.app_context():
        with pytest.raises(ValueError):
            Exercise(name="Lunges", category="not_real")


def test_workout_duration_validation(client):
    with app.app_context():
        with pytest.raises(ValueError):
            Workout(date="2026-07-01", duration_minutes=-5, notes="bad")


def test_get_workouts_empty(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout(client):
    response = client.post("/workouts", json={
        "date": "2026-07-01",
        "duration_minutes": 30,
        "notes": "Test workout"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["duration_minutes"] == 30


def test_create_workout_invalid_duration(client):
    response = client.post("/workouts", json={
        "date": "2026-07-01",
        "duration_minutes": -10,
        "notes": "Bad workout"
    })
    assert response.status_code == 400


def test_get_workout_not_found(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_create_exercise(client):
    response = client.post("/exercises", json={
        "name": "Deadlift",
        "category": "strength",
        "equipment_needed": True
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Deadlift"


def test_create_exercise_invalid_category(client):
    response = client.post("/exercises", json={
        "name": "Deadlift",
        "category": "not_real"
    })
    assert response.status_code == 400


def test_delete_workout_not_found(client):
    response = client.delete("/workouts/999")
    assert response.status_code == 404


def test_link_exercise_to_workout(client):
    workout_resp = client.post("/workouts", json={
        "date": "2026-07-01",
        "duration_minutes": 30,
        "notes": None
    })
    exercise_resp = client.post("/exercises", json={
        "name": "Squat",
        "category": "strength"
    })
    workout_id = workout_resp.get_json()["id"]
    exercise_id = exercise_resp.get_json()["id"]

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"reps": 10, "sets": 3}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["reps"] == 10
    assert data["sets"] == 3