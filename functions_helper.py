from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from habit import Habit
import json
import uuid

def day_check(last_updated_at):
    """
    Check if the last updated date is the same as today, one day before today, or earlier.

    Parameters:
    last_updated_at (datetime): The last updated date of the habit.

    Returns:
    str: "Same", "Valid Date", or "Streak Expired" based on the date comparison.
    """
    if last_updated_at.date() == datetime.now().date():
        return "Same"
    elif last_updated_at.date() + timedelta(days=1) == datetime.now().date():
        return "Valid Date"
    elif last_updated_at.date() + timedelta(days=1) < datetime.now().date():
        return "Streak Expired"

def week_check(last_updated_at):
    """
    Check if the last updated date is the same week as today, one week before today, or earlier.

    Parameters:
    last_updated_at (datetime): The last updated date of the habit.

    Returns:
    str: "Same", "Valid", or "Streak Expired" based on the date comparison.
    """
    if last_updated_at.isocalendar()[1] == datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Same"
    elif last_updated_at.isocalendar()[1] + 1 == datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Valid"
    elif last_updated_at.isocalendar()[1] + 1 < datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Streak Expired"

def month_check(last_updated_at):
    """
    Check if the last updated date is the same month as today, one month before today, or earlier.

    Parameters:
    last_updated_at (datetime): The last updated date of the habit.

    Returns:
    str: "Same", "Valid", or "Streak Expired" based on the date comparison.
    """
    if last_updated_at.month == datetime.now().month and last_updated_at.year == datetime.now().year:
        return "Same"
    elif last_updated_at.month + 1 == datetime.now().month + 1 and last_updated_at.year == datetime.now().year:
        return "Valid"
    elif last_updated_at.month > datetime.now().month + 1 and last_updated_at.year == datetime.now().year:
        return "Streak Expired"

def date_check_with_periodicity(periodicity, last_updated_at):
    """
    Check the date with respect to the given periodicity.

    Parameters:
    periodicity (str): The periodicity of the habit ('D', 'W', 'M').
    last_updated_at (datetime): The last updated date of the habit.

    Returns:
    str: The status of the habit based on the date check.
    """
    if not isinstance(last_updated_at, datetime):
        last_updated_at = datetime.fromisoformat(last_updated_at)
    if periodicity == 'D':
        return day_check(last_updated_at)
    elif periodicity == 'W':
        return week_check(last_updated_at)
    elif periodicity == 'M':
        return month_check(last_updated_at)

def check_max_streak(periodicity, created_at, last_updated_at):
    """
    Calculate the maximum streak based on periodicity.

    Parameters:
    periodicity (str): The periodicity of the habit ('D', 'W', 'M').
    created_at (datetime): The creation date of the habit.
    last_updated_at (datetime): The last updated date of the habit.

    Returns:
    int: The maximum streak.
    """
    if periodicity == 'D':
        return (last_updated_at - created_at).days
    elif periodicity == 'W':
        return (last_updated_at - created_at).days // 7
    elif periodicity == 'M':
        return (last_updated_at.year - created_at.year) * 12 + last_updated_at.month - created_at.month

def create_initial_habits():
    """Create initial habits from predefined data."""
    with open('test_data/predefined_habits.json', 'r') as f:
        predefined_habits = json.load(f)

    for habit_data in predefined_habits:
        last_updated_at = datetime.now() - timedelta(days=random.randint(1, 10))
        created_at = last_updated_at - timedelta(days=random.randint(365, 730))
        max_streak = check_max_streak(habit_data["periodicity"], created_at, last_updated_at)
        if date_check_with_periodicity(habit_data["periodicity"], last_updated_at) != "Streak Expired":
            if max_streak != 0:
                streak = random.randint(1, max_streak)
            else:
                streak = 0 
        if date_check_with_periodicity(habit_data["periodicity"], last_updated_at) == "Streak Expired":
            streak = 0
        habit = Habit(
            habit_id=uuid.uuid4(),
            name=habit_data["name"], 
            periodicity=habit_data["periodicity"],
            created_at=created_at,
            streak=streak,
            last_updated_at=last_updated_at
        )
        success = habit.create_habit()
        if not success:
            print(f"Habit {habit_data['name']} already exists.")
            continue
        dates = generate_random_habit_tracking_dates(
            periodicity=habit_data["periodicity"],
            created_at=created_at,
            streak=streak,
            last_updated_at=last_updated_at,
            success_rate=habit_data["success_rate"]
        )
        print(f"Generating {len(dates)} random dates of tracking data for habit {habit_data['name']}")
        for date in dates:
            habit.mark_habit_as_completed(write_date=datetime.fromisoformat(date), is_fake_tracking_data=True)

def generate_random_habit_tracking_dates(periodicity, created_at, streak, last_updated_at, success_rate=0.8):
    """
    Generate random tracking dates based on periodicity and success rate.

    Parameters:
    periodicity (str): The periodicity of the habit ('D', 'W', 'M').
    created_at (datetime): The creation date of the habit.
    streak (int): The current streak of the habit.
    last_updated_at (datetime): The last updated date of the habit.
    success_rate (float): The success rate of the habit.

    Returns:
    list: A list of dates when the habit was tracked.
    """
    if periodicity == 'D':
        diff = (last_updated_at - created_at).days
        dates_list = [(created_at + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(diff + 1)]
    elif periodicity == 'W':
        dates_list = []
        current_date = created_at
        while current_date <= last_updated_at:
            week_start = current_date - relativedelta(days=current_date.weekday())
            week_end = min(last_updated_at, week_start + timedelta(days=6))
            random_date = week_start + timedelta(days=random.randint(0, (week_end - week_start).days))
            dates_list.append(random_date.strftime('%Y-%m-%d'))
            current_date = week_end + timedelta(days=1)
    elif periodicity == 'M':
        dates_list = []
        current_date = created_at
        while current_date <= last_updated_at:
            month_start = current_date.replace(day=1)
            next_month = month_start + relativedelta(months=1)
            month_end = min(last_updated_at, next_month - timedelta(days=1))
            random_date = month_start + timedelta(days=random.randint(0, (month_end - month_start).days))
            dates_list.append(random_date.strftime('%Y-%m-%d'))
            current_date = next_month

    if streak == 0:
        if periodicity == 'D':
            dates_list = dates_list[:-1]
        elif periodicity == 'W':
            dates_list = dates_list[:-7]
        elif periodicity == 'M':
            dates_list = dates_list[:-31]

    # elements that can be dropped out
    non_streak_elements = dates_list[:-streak] if streak > 0 else dates_list
    non_streak_elements = non_streak_elements[:-1]
    
    # elements that must be kept
    streak_elements = dates_list[-streak:] if streak > 0 else []

    dropout_count = int(len(non_streak_elements) * (1 - success_rate))
    dropout_indices = random.sample(range(len(non_streak_elements)), dropout_count)
    non_streak_elements = [date for i, date in enumerate(non_streak_elements) if i not in dropout_indices]

    dates_list = non_streak_elements + streak_elements

    return dates_list

def generate_tracking_data_dict(tracking_data, periodicity):
    """
    Generate a dictionary of tracking data based on periodicity.

    Parameters:
    tracking_data (list): A list of tracking dates.
    periodicity (str): The periodicity of the habit ('D', 'W', 'M').

    Returns:
    dict: A dictionary with years as keys and tracking data as values.
    """
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in tracking_data]
    
    tracking_dict = {}
    for date in dates:
        year = date.year
        if year not in tracking_dict:
            is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            days_in_year = 366 if is_leap_year else 365
            tracking_dict[year] = [0] * days_in_year
    
    for date in dates:
        year = date.year
        start_of_year = datetime(year, 1, 1)
        day_of_year = (date - start_of_year).days
        
        if periodicity == 'D':
            tracking_dict[year][day_of_year] = 1
        elif periodicity == 'W':
            start_of_week = date - timedelta(days=date.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            for i in range((start_of_week - start_of_year).days, (end_of_week - start_of_year).days + 1):
                if 0 <= i < len(tracking_dict[year]):
                    tracking_dict[year][i] = 1
        elif periodicity == 'M':
            start_of_month = datetime(year, date.month, 1)
            if date.month == 12:
                end_of_month = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_of_month = datetime(year, date.month + 1, 1) - timedelta(days=1)
            for i in range((start_of_month - start_of_year).days, (end_of_month - start_of_year).days + 1):
                if 0 <= i < len(tracking_dict[year]):
                    tracking_dict[year][i] = 1
    
    return tracking_dict
