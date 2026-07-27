from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(ValidationError)
def validation_error(error):
    return make_response(jsonify({'errors': error.messages}), 400)

# Workout endpoints
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    return make_response(workout_schema.dump(workout), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        workout = Workout(**workout_schema.load(data))
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    for we in workout.workout_exercises:
        db.session.delete(we)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({'message': 'Workout deleted'}), 200)

# Exercise endpoints
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    return make_response(exercise_schema.dump(exercise), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()
        exercise = Exercise(**exercise_schema.load(data))
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    for we in exercise.workout_exercises:
        db.session.delete(we)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({'message': 'Exercise deleted'}), 200)

# WorkoutExercise endpoint
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        if not Workout.query.get(workout_id):
            return make_response(jsonify({'error': 'Workout not found'}), 404)
        if not Exercise.query.get(exercise_id):
            return make_response(jsonify({'error': 'Exercise not found'}), 404)
        
        data = request.get_json()
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        we = WorkoutExercise(**workout_exercise_schema.load(data))
        db.session.add(we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(we), 201)
    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
