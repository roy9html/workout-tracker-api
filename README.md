 # Tree
text
workout-tracker-api/
├── .git/
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
├── test_api.sh
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    ├── instance/
    │   └── app.db
    └── migrations/
        ├── alembic.ini
        ├── env.py
        ├── README
        ├── script.py.mako
        └── versions/
            └── [timestamp]_initial_migration.py
 Complete README.md for Submission
Update your README.md with this complete version:

bash
cat > README.md << 'EOF'
#  Workout Tracker API

# Project Description
A RESTful API for a workout tracking application designed for personal trainers. The API allows trainers to manage workouts and exercises, track sets, reps, and duration for each exercise within a workout. Built with Flask, SQLAlchemy, and Marshmallow, it provides robust data validation and serialization.

# Features
. Create, view, and delete workouts
. Create, view, and delete exercises
. Add exercises to workouts with sets, reps, and duration tracking
. Comprehensive data validation at model, schema, and database levels
. Many-to-many relationships between workouts and exercises
. Structured error handling and response formatting

# Technologies Used
. Python 3.8.13+
. Flask 2.2.2
. Flask-SQLAlchemy 3.0.3
. Flask-Migrate 3.1.0
. Marshmallow 3.20.1
. SQLite (development database)
. Pipenv for dependency management

# Installation Instructions

# Prerequisites
. Python 3.8.13 or higher
. Pipenv

# Setup

1. Clone the repository:
 bash
git clone https://github.com/roy9html/workout-tracker-api.git
cd workout-tracker-api
Install dependencies using Pipenv:

bash
pipenv install
Activate the virtual environment:

bash
pipenv shell
Navigate to the server directory:

bash
cd server
Initialize and migrate the database:

bash
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade head
Seed the database with sample data:

bash
python seed.py
  Run Instructions
Start the Flask development server:

bash
python -m flask run --port=5555
Or run directly:

bash
python app.py
The API will be available at http://localhost:5555

 API Endpoints
Workouts
Method	Endpoint	Description
GET	/workouts	List all workouts
GET	/workouts/<id>	Get a specific workout with its exercises
POST	/workouts	Create a new workout
DELETE	/workouts/<id>	Delete a workout and its associations
Exercises
Method	Endpoint	Description
GET	/exercises	List all exercises
GET	/exercises/<id>	Get a specific exercise with its workouts
POST	/exercises	Create a new exercise
DELETE	/exercises/<id>	Delete an exercise and its associations
WorkoutExercises (Join Table)
Method	Endpoint	Description
POST	/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises	Add an exercise to a workout with reps/sets/duration
 Request/Response Examples
Create a Workout
Request:

bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-07-28","duration_minutes":45,"notes":"Morning workout"}'
Response:

json
{
  "date": "2026-07-28",
  "duration_minutes": 45,
  "id": 1,
  "notes": "Morning workout"
}
Create an Exercise
Request:

bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Bench Press","category":"Strength","equipment_needed":true}'
Response:

json
{
  "category": "Strength",
  "equipment_needed": true,
  "id": 1,
  "name": "Bench Press"
}
Add Exercise to Workout
Request:

bash
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps":10,"sets":3}'
Response:

json
{
  "duration_seconds": null,
  "exercise_id": 1,
  "id": 1,
  "reps": 10,
  "sets": 3,
  "workout_id": 1
}
 Testing
Run the test script:

bash
 test individual endpoints with curl:

bash
# Get all workouts
curl http://localhost:5555/workouts

# Get all exercises
curl http://localhost:5555/exercises

# Get workout with exercises
curl http://localhost:5555/workouts/1
 Data Validation
Table Constraints (Database Level)
Exercise: name minimum 3 characters, valid category types

Workout: positive duration, date not in future

WorkoutExercise: positive reps/sets/duration, at least reps or duration

Model Validations (Application Level)
Exercise: name length ≥ 3, valid category

Workout: date not future, duration > 0

WorkoutExercise: positive values for reps/sets/duration

Schema Validations (API Level)
Exercise: name length ≥ 3, valid category

Workout: date not future, duration in valid range (1-1440 minutes)

WorkoutExercise: at least reps or duration, sets with reps, value ranges

 License
This project is for educational purposes as part of a software development course.
EOF

text

# Final Submission Commands

bash
# 1. Make sure all changes are committed
git status
git add .
git commit -m "chore: finalize project for submission"

# 2. Push to GitHub
git push origin main
git push origin develop
git push origin release/v1.0.0

# 3. Verify everything is on GitHub
git branch -a
git log --oneline -5

