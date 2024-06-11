from flask import Flask, request, jsonify, render_template
from habit import Habit
from db import Database
from datetime import datetime, timedelta
import random
from functions_helper import date_check_with_periodicity, check_max_streak, create_initial_habits

app = Flask(__name__)

db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_initial_habits', methods=['POST'])
def create_initial_habits_route():
    create_initial_habits()
    return jsonify({'status': 'success'})

@app.route('/clear_habits_table', methods=['POST'])
def clear_habits_table_route():
    db.clear_habits_table()
    return jsonify({'status': 'success'})

@app.route('/habits', methods=['GET'])
def get_habits():
    habit = Habit()
    habits = habit.get_all_habits()
    return jsonify(habits)

@app.route('/habits/<string:name>', methods=['GET'])
def get_habit(name):
    habit = Habit(name=name)
    habit = habit.get_habit_from_name()
    return jsonify(habit)

@app.route('/habits', methods=['POST'])
def create_habit():
    data = request.json
    name = data['name'].title()
    if name == '':
        return jsonify({'message': 'Habit name cannot be empty'}), 400
    periodicity = data['periodicity']
    habit = Habit(name=name, periodicity=periodicity, created_at=datetime.now(), streak=0, last_updated_at=datetime.now())
    habit.create_habit()
    return jsonify({'message': 'Habit created successfully'})

@app.route('/habits/<string:name>', methods=['DELETE'])
def delete_habit(name):
    habit = Habit(name=name)
    habit.get_habit_from_name()
    habit.delete_habit()
    return jsonify({'message': f'Habit {name} deleted successfully'})

@app.route('/habits/<string:name>', methods=['PUT'])
def mark_habit_as_completed(name):
    habit = Habit(name=name)
    habit.get_habit_from_name()
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
