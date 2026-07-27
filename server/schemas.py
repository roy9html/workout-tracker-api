from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import datetime

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()
    
    @validates('name')
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise ValidationError('Name must be at least 3 characters')
    
    @validates('category')
    def validate_category(self, value):
        valid = ['Strength', 'Cardio', 'Flexibility', 'Balance']
        if value not in valid:
            raise ValidationError(f'Category must be one of: {", ".join(valid)}')

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)
    exercises = fields.Nested('ExerciseSchema', many=True, dump_only=True)
    
    @validates('date')
    def validate_date(self, value):
        if value > datetime.now().date():
            raise ValidationError('Date cannot be in the future')
    
    @validates('duration_minutes')
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError('Duration must be > 0')
        if value > 1440:
            raise ValidationError('Duration cannot exceed 1440 minutes')

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    workout = fields.Nested('WorkoutSchema', dump_only=True)
    exercise = fields.Nested('ExerciseSchema', dump_only=True)
    
    @validates_schema
    def validate_reps_or_duration(self, data, **kwargs):
        reps = data.get('reps')
        duration = data.get('duration_seconds')
        sets = data.get('sets')
        
        if reps is None and duration is None:
            raise ValidationError('Must provide reps or duration_seconds')
        
        if reps is not None and sets is None:
            raise ValidationError('When providing reps, sets must also be provided')
        
        if sets is not None and reps is None:
            raise ValidationError('When providing sets, reps must also be provided')
    
    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Reps must be > 0')
        if value is not None and value > 100:
            raise ValidationError('Reps cannot exceed 100')
    
    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Sets must be > 0')
        if value is not None and value > 20:
            raise ValidationError('Sets cannot exceed 20')
    
    @validates('duration_seconds')
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Duration must be > 0')
        if value is not None and value > 7200:
            raise ValidationError('Duration cannot exceed 7200 seconds')

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
