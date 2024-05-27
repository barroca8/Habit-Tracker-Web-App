from flask import Flask, request, jsonify, render_template
from habit import Habit
from db import Database
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habits', methods=['GET'])
def get_habits():
    habit = Habit()
    habits = habit.get_all_habits()
    return jsonify(habits)

@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.json
    name = data['name'].title()
    periodicity = data['periodicity']
    habit = Habit(name=name, periodicity=periodicity, created_at=datetime.now(), streak=0, last_updated_at=datetime.now())
    habit.create_habit()
    return jsonify({'message': 'Habit created successfully'})

@app.route('/habits/<string:name>', methods=['DELETE'])
def delete_habit(name):
    habit = Habit(name=name, periodicity=None, created_at=None, streak=None, last_updated_at=None)
    habit.delete_habit()
    return jsonify({'message': f'Habit {name} deleted successfully'})

@app.route('/streaks/daily', methods=['GET'])
def get_longest_daily_streak():
    habit = Habit()
    streak = habit.longest_daily_streak()
    return jsonify(streak)

@app.route('/streaks/weekly', methods=['GET'])
def get_longest_weekly_streak():
    habit = Habit()
    streak = habit.longest_weekly_streak()
    return jsonify(streak)

@app.route('/streaks/monthly', methods=['GET'])
def get_longest_monthly_streak():
    habit = Habit()
    streak = habit.longest_monthly_streak()
    return jsonify(streak)

if __name__ == '__main__':
    db = Database()
    db.clear_habits_table()
    predefined_habits = [
        {"name": "Brush Teeth", "periodicity": "D"},
        {"name": "Exercise", "periodicity": "D"},
        {"name": "Read Book", "periodicity": "W"},
        {"name": "Call Family", "periodicity": "W"},
        {"name": "Grocery Shopping", "periodicity": "M"}
    ]
    for habit_data in predefined_habits:
        habit = Habit(name=habit_data["name"], periodicity=habit_data["periodicity"], created_at=datetime.now(), streak=0, last_updated_at=datetime.now())
        habit.create_habit()
    app.run(debug=True)