from flask import Flask, request, jsonify, render_template
from habit import Habit
from db import Database
from datetime import datetime
from functions_helper import date_check_with_periodicity, create_initial_habits, generate_tracking_data_dict
import uuid

app = Flask(__name__)

db = Database()

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/create_initial_habits', methods=['POST'])
def create_initial_habits_route():
    """Create initial habits from predefined data."""
    create_initial_habits()
    return jsonify({'status': 'success'})

@app.route('/clear_habits_table', methods=['POST'])
def clear_habits_table_route():
    """Clear the habits table."""
    db.clear_habits_table()
    return jsonify({'status': 'success'})

@app.route('/habits', methods=['GET'])
def get_habits():
    """Get all habits from the database."""
    habit = Habit()
    habits = habit.get_all_habits()
    return jsonify(habits)

@app.route('/habits/<string:name>', methods=['GET'])
def get_habit(name):
    """
    Get a habit by name.

    Parameters:
    name (str): The name of the habit to retrieve.

    Returns:
    JSON: The habit data.
    """
    habit = Habit(name=name)
    habit = habit.get_habit_from_name()
    return jsonify(habit)

@app.route('/habits', methods=['POST'])
def create_habit():
    """
    Create a new habit.

    Returns:
    JSON: Success or error message.
    """
    data = request.json
    name = data['name'].title()
    if name == '':
        return jsonify({'message': 'Habit name cannot be empty'}), 400
    periodicity = data['periodicity']
    habit = Habit(
        habit_id=uuid.uuid4(), 
        name=name, 
        periodicity=periodicity, 
        created_at=datetime.now(), 
        streak=0, 
        last_updated_at=datetime.now()
    )
    success = habit.create_habit()
    if success:
        return jsonify({'message': 'Habit created successfully'})
    else:
        return jsonify({'message': 'Habit already exists'}), 400

@app.route('/habits/<string:name>', methods=['DELETE'])
def delete_habit(name):
    """
    Delete a habit by name.

    Parameters:
    name (str): The name of the habit to delete.

    Returns:
    JSON: Success message.
    """
    habit = Habit(name=name)
    habit.get_habit_from_name()
    habit.delete_habit()
    return jsonify({'message': f'Habit {name} deleted successfully'})

@app.route('/habits/<string:name>', methods=['PUT'])
def mark_habit_as_completed(name):
    """
    Mark a habit as completed.

    Parameters:
    name (str): The name of the habit to mark as completed.

    Returns:
    JSON: Success message.
    """
    habit = Habit(name=name)
    habit.get_habit_from_name()
    habit.mark_habit_as_completed()
    return jsonify({'message': f'Habit {name} marked as completed'})

@app.route('/habits/check/', methods=['GET'])
def update_marked_status():
    """
    Check the marked status of a habit.

    Returns:
    JSON: The status of the habit.
    """
    periodicity = request.args.get('periodicity')
    last_updated_at = request.args.get('last_updated_at')
    status = date_check_with_periodicity(periodicity, last_updated_at)
    return jsonify(status)

@app.route('/habits/tracking/<string:habit_id>', methods=['GET'])
def get_habit_tracking(habit_id):
    """
    Get tracking data for a habit.

    Parameters:
    habit_id (str): The ID of the habit.

    Returns:
    JSON: The tracking data.
    """
    habit = Habit(habit_id=habit_id)
    tracking_data, periodicity = habit.get_tracking_data()
    tracking_data = generate_tracking_data_dict(tracking_data, periodicity)
    return jsonify(tracking_data)

@app.route('/streaks/daily', methods=['GET'])
def get_longest_daily_streak():
    """
    Get the longest daily streak.

    Returns:
    JSON: The longest daily streak.
    """
    habit = Habit()
    streak = habit.longest_daily_streak()
    return jsonify(streak)

@app.route('/streaks/weekly', methods=['GET'])
def get_longest_weekly_streak():
    """
    Get the longest weekly streak.

    Returns:
    JSON: The longest weekly streak.
    """
    habit = Habit()
    streak = habit.longest_weekly_streak()
    return jsonify(streak)

@app.route('/streaks/monthly', methods=['GET'])
def get_longest_monthly_streak():
    """
    Get the longest monthly streak.

    Returns:
    JSON: The longest monthly streak.
    """
    habit = Habit()
    streak = habit.longest_monthly_streak()
    return jsonify(streak)
