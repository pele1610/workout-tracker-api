#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Creating exercises...")
    pushups = Exercise(name="Push-up", category="strength", equipment_needed=False)
    squats = Exercise(name="Squat", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)

    db.session.add_all([pushups, squats, running, bench_press])
    db.session.commit()

    print("Creating workouts...")
    workout_1 = Workout(date=date(2026, 7, 1), duration_minutes=45, notes="Morning strength session")
    workout_2 = Workout(date=date(2026, 7, 3), duration_minutes=30, notes="Quick cardio")

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=pushups.id, reps=15, sets=3, duration_seconds=None)
    we2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=squats.id, reps=12, sets=3, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=workout_1.id, exercise_id=bench_press.id, reps=8, sets=4, duration_seconds=None)
    we4 = WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, reps=None, sets=None, duration_seconds=1200)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Done seeding!")

    