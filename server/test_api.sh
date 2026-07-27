#!/bin/bash
echo "=== WORKOUT TRACKER API TEST ==="
echo ""

echo "1. GET all workouts:"
curl -s http://localhost:5555/workouts | python -m json.tool
echo ""

echo "2. GET all exercises:"
curl -s http://localhost:5555/exercises | python -m json.tool
echo ""

echo "3. POST create workout:"
curl -s -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-07-28","duration_minutes":45,"notes":"Test workout"}' \
  | python -m json.tool
echo ""

echo "4. POST create exercise:"
curl -s -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Push-ups","category":"Strength","equipment_needed":false}' \
  | python -m json.tool
echo ""

echo "5. POST add exercise to workout:"
curl -s -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps":12,"sets":3}' \
  | python -m json.tool
echo ""

echo "6. GET workout with exercises:"
curl -s http://localhost:5555/workouts/1 | python -m json.tool
echo ""

echo "=== TEST COMPLETE ==="
