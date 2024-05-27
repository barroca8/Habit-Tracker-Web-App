from flask import Flask, request, jsonify, render_template
from habit import Habit
from db import Database
from datetime import datetime, timedelta
import random
from functions_helper import date_check_with_periodicity, check_max_streak

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habits', methods=['GET'])
def get_habits():
    habit = Habit()
    habits = habit.get_all_habits()
    return jsonify(habits)

@app.route('/habits/<string:name>', methods=['GET'])
def get_habit(name):
    habit = Habit()
    habit = habit.get_habit_from_name(name)
    return jsonify(habit)

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

@app.route('/habits/<string:name>', methods=['PUT'])
def mark_habit_as_completed(name):
    habit = Habit(name=name)
    habit.get_habit_from_name(name)
    habit.mark_habit_as_completed()
    return jsonify({'message': f'Habit {name} marked as completed'})

@app.route('/habits/check/', methods=['GET'])
def update_marked_status():
    periodicity = request.args.get('periodicity')
    last_updated_at = request.args.get('last_updated_at')
    status = date_check_with_periodicity(periodicity, last_updated_at)
    return jsonify(status)

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
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        last_updated_at = datetime.now() - timedelta(days=random.randint(1, 10))
        max_streak = check_max_streak(habit_data["periodicity"], created_at, last_updated_at)
        if date_check_with_periodicity(habit_data["periodicity"], last_updated_at) != "Streak Expired":
            # TODO: max_streak is sometimes -1, when periodicity is weekly
            if max_streak != 0:
                print(max_streak)
                streak = random.randint(1, max_streak)
            else:
                streak = 0 
        if date_check_with_periodicity(habit_data["periodicity"], last_updated_at) == "Streak Expired":
            streak = 0
        habit = Habit(
            name=habit_data["name"], 
            periodicity=habit_data["periodicity"],
            created_at=created_at,
            streak=streak,
            last_updated_at=last_updated_at
        )
        habit.create_habit()
    app.run(debug=True)