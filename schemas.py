from marshmallow import Schema, fields, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean()

    @validates("name")
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty")

    @validates("category")
    def validate_category(self, value):
        allowed = ["strength", "cardio", "flexibility", "balance"]
        if value not in allowed:
            raise ValidationError(f"category must be one of {allowed}")


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True)
    notes = fields.String(allow_none=True)

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("duration_minutes must be greater than 0")


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError("reps cannot be negative")

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value < 0:
            raise ValidationError("sets cannot be negative")