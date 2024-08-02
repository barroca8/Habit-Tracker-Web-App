from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from habit import Habit
import json
import uuid

def day_check(last_updated_at):
    if last_updated_at.date() == datetime.now().date():
        return "Same"
    elif last_updated_at.date() + timedelta(days=1) == datetime.now().date():
        return "Valid Date"
    elif last_updated_at.date() + timedelta(days=1) < datetime.now().date():
        return "Streak Expired"

def week_check(last_updated_at):
    if last_updated_at.isocalendar()[1] == datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Same"
    elif last_updated_at.isocalendar()[1] + 1 == datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Valid"
    elif last_updated_at.isocalendar()[1] + 1 < datetime.now().isocalendar()[1] and last_updated_at.year == datetime.now().year:
        return "Streak Expired"

def month_check(last_updated_at):
    if last_updated_at.month == datetime.now().month and last_updated_at.year == datetime.now().year:
        return "Same"
    elif last_updated_at.month + 1 == datetime.now().month + 1 and last_updated_at.year == datetime.now().year:
        return "Valid"
    elif last_updated_at.month > datetime.now().month + 1 and last_updated_at.year == datetime.now().year:
        return "Streak Expired"

def date_check_with_periodicity(periodicity, last_updated_at):
    if not isinstance(last_updated_at, datetime):
        last_updated_at = datetime.fromisoformat(last_updated_at)
    if periodicity == 'D':
        return day_check(last_updated_at)
    elif periodicity == 'W':
        return week_check(last_updated_at)
    elif periodicity == 'M':
        return month_check(last_updated_at)

def check_max_streak(periodicity, created_at, last_updated_at):
    if periodicity == 'D':
        return (last_updated_at - created_at).days
    elif periodicity == 'W':
        return (last_updated_at - created_at).days // 7
    elif periodicity == 'M':
        return (last_updated_at.year - created_at.year) * 12 + last_updated_at.month - created_at.month

def create_initial_habits():
    with open('predefined_habits.json', 'r') as f:
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
        habit.create_habit()
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
    if periodicity == 'D':
        diff = (last_updated_at - created_at).days
        dates_list = [(created_at + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(diff + 1)]
    elif periodicity == 'W':
        dates_list = []
        current_date = created_at
        while current_date <= last_updated_at:
            week_start = current_date
            week_end = min(last_updated_at, week_start + timedelta(days=6))
            random_date = week_start + timedelta(days=random.randint(0, (week_end - week_start).days))
            dates_list.append(random_date.strftime('%Y-%m-%d'))
            current_date = week_end + timedelta(days=1)
    elif periodicity == 'M':
        dates_list = []
        current_date = created_at
        while current_date <= last_updated_at:
            month_start = current_date
            next_month = month_start + relativedelta(months=1)
            month_end = min(last_updated_at, next_month - timedelta(days=1))
            random_date = month_start + timedelta(days=random.randint(0, (month_end - month_start).days))
            dates_list.append(random_date.strftime('%Y-%m-%d'))
            current_date = next_month

    if streak == 0:
        dates_list = dates_list[:-1]
    else:
        dates_list = dates_list[-streak:]

    dropout_count = int(len(dates_list) * (1 - success_rate))
    dropout_indices = random.sample(range(len(dates_list)), dropout_count)
    dates_list = [date for i, date in enumerate(dates_list) if i not in dropout_indices]

    return dates_list
