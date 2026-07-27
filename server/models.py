from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import datetime

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    __table_args__ = (
        CheckConstraint('length(name) >= 3', name='exercise_name_min_length'),
        CheckConstraint("category IN ('Strength', 'Cardio', 'Flexibility', 'Balance')", 
                       name='exercise_category_valid'),
    )
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError('Name must be at least 3 characters')
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        valid = ['Strength', 'Cardio', 'Flexibility', 'Balance']
        if category not in valid:
            raise ValueError(f'Category must be one of: {", ".join(valid)}')
        return category

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='workout_duration_positive'),
        CheckConstraint('date <= CURRENT_DATE', name='workout_date_not_future'),
    )
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')
    
    @validates('date')
    def validate_date(self, key, date):
        if date > datetime.now().date():
            raise ValueError('Date cannot be in the future')
        return date
    
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError('Duration must be > 0')
        return duration

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    
    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps > 0', name='reps_positive'),
        CheckConstraint('sets IS NULL OR sets > 0', name='sets_positive'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='duration_positive'),
        CheckConstraint('(reps IS NOT NULL OR duration_seconds IS NOT NULL)', name='reps_or_duration'),
    )
    
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError('Reps must be > 0')
        return reps
    
    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError('Sets must be > 0')
        return sets
    
    @validates('duration_seconds')
    def validate_duration(self, key, duration):
        if duration is not None and duration <= 0:
            raise ValueError('Duration must be > 0')
        return duration
