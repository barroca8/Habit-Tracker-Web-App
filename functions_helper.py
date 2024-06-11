from datetime import datetime, timedelta
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
    # if last_updated_at isn't a datetime object, convert it to one
    if not isinstance(last_updated_at, datetime):
        last_updated_at = datetime.fromisoformat(last_updated_at)
    if periodicity == 'D':
        return day_check(last_updated_at)
    elif periodicity == 'W':
        return week_check(last_updated_at)
    elif periodicity == 'M':
        return month_check(last_updated_at)

# Same - button disabled
# Valid - button enabled, streak active
# Streak Expired - button enabled, streak expired (streak needs to be set to 0)

def check_max_streak(periodicity, created_at, last_updated_at):
    if periodicity == 'D':
        return (last_updated_at - created_at).days
    elif periodicity == 'W':
        return (last_updated_at - created_at).days // 7
    elif periodicity == 'M':
        return (last_updated_at.year - created_at.year) * 12 + last_updated_at.month - created_at.month

def create_initial_habits():
    
    with open('test_data/predefined_habits.json', 'r') as f:
        predefined_habits = json.load(f)

    # TODO: use habit_tracking table to know the streaks
    # TODO: generate random values for habit_tracking for 1 year of tracking of the predefined_habits
    for habit_data in predefined_habits:
        last_updated_at = datetime.now() - timedelta(days=random.randint(1, 10))
        created_at = last_updated_at - timedelta(days=random.randint(1, 365))
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


def fill_habit_tracking_data(
    habit_id: str,
    name: str,
    periodicity: str,
    created_at: datetime,
    streak: int,
    last_updated_at: datetime
):
    
    
    if periodicity == 'D':
        # generate a range of all dates between created_at and last_updated_at
        diff = (last_updated_at - created_at).days
        dates_list = [(created_at + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(diff)]
        print(dates_list)
        pass

    if periodicity == 'W':
        # generate a range of one date per week between created_at and last_updated_at
        diff = (last_updated_at - created_at).days // 7
        dates_list = [(created_at + timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(diff)]
        print(dates_list)
        # TODO: search how to generate a random date in a week
        pass

    if periodicity == 'M':
        # generate a range of one date per month between created_at and last_updated_at
        diff = (last_updated_at.year - created_at.year) * 12 + last_updated_at.month - created_at.month
        dates_list = [(created_at + timedelta(months=i)).strftime('%Y-%m-%d') for i in range(diff)]
        # TODO: timedelta(months=i) doesn't work
        # TODO: search how to generate a random date in a month
        print(dates_list)
        pass

    # if streak != 0, we need to make sure that streak is reflected in this list of dates
    # after the streak is assured, we need to make sure we break the streak on the date just before the streak is assured
    # the rest of the dates are randomized, choosing about 20% of those dates (percentage to decide later)
    # all the values are written to habit_tracking, using the uuid and the date
    # TODO: this makes the streak column be redundant, as it can be gotten from a simple count in this table. reconsider habits structure


if __name__ == '__main__':
    fill_habit_tracking_data(
        habit_id='test_uuid',
        name='test_name',
        periodicity='M',
        created_at=datetime(2024,5,1),
        streak=30,
        last_updated_at=datetime.now()
    )








