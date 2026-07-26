from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", overlaps="workouts,exercises"
    )
    workouts = db.relationship(
        "Workout", secondary="workout_exercises", back_populates="exercises", overlaps="workout_exercises"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        return value

    @validates("category")
    def validate_category(self, key, value):
        allowed = ["strength", "cardio", "flexibility", "balance"]
        if value not in allowed:
            raise ValueError(f"category must be one of {allowed}")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", overlaps="exercises,workouts"
    )
    exercises = db.relationship(
        "Exercise", secondary="workout_exercises", back_populates="workouts", overlaps="workout_exercises"
    )

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="check_duration_positive"),
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship(
        "Workout", back_populates="workout_exercises", overlaps="exercises,workouts"
    )
    exercise = db.relationship(
        "Exercise", back_populates="workout_exercises", overlaps="exercises,workouts"
    )

    __table_args__ = (
        db.CheckConstraint("reps >= 0", name="check_reps_non_negative"),
        db.CheckConstraint("sets >= 0", name="check_sets_non_negative"),
    )