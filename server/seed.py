#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

def seed():
    with app.app_context():
        db.session.query(WorkoutExercise).delete()
        db.session.query(Exercise).delete()
        db.session.query(Workout).delete()
        
        exercises = [
            Exercise(name='Bench Press', category='Strength', equipment_needed=True),
            Exercise(name='Squat', category='Strength', equipment_needed=True),
            Exercise(name='Deadlift', category='Strength', equipment_needed=True),
            Exercise(name='Push-ups', category='Strength', equipment_needed=False),
            Exercise(name='Pull-ups', category='Strength', equipment_needed=False),
            Exercise(name='Running', category='Cardio', equipment_needed=False),
            Exercise(name='Cycling', category='Cardio', equipment_needed=True),
            Exercise(name='Yoga', category='Flexibility', equipment_needed=False),
        ]
        for ex in exercises:
            db.session.add(ex)
        
        workouts = [
            Workout(date=date.today(), duration_minutes=45, notes='Upper body'),
            Workout(date=date.today()-timedelta(days=2), duration_minutes=60, notes='Leg day'),
            Workout(date=date.today()-timedelta(days=4), duration_minutes=30, notes='Cardio'),
        ]
        for wo in workouts:
            db.session.add(wo)
        
        db.session.commit()
        
        wes = [
            WorkoutExercise(workout_id=1, exercise_id=1, reps=10, sets=3),
            WorkoutExercise(workout_id=1, exercise_id=4, reps=15, sets=3),
            WorkoutExercise(workout_id=2, exercise_id=2, reps=12, sets=4),
            WorkoutExercise(workout_id=2, exercise_id=3, reps=8, sets=3),
            WorkoutExercise(workout_id=3, exercise_id=6, duration_seconds=1800),
        ]
        for we in wes:
            db.session.add(we)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
