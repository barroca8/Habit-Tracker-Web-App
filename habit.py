from db import Database
from datetime import datetime

class Habit:
    def __init__(self, name=None, periodicity=None, created_at=None, streak=None, last_updated_at=None):
        self.name = name.title() if name else name
        self.periodicity = periodicity
        self.created_at = created_at
        self.streak = streak
        self.last_updated_at = last_updated_at

    def create_habit(self):
        db = Database()
        if db.habit_exists(self.name):
            print(f"Habit {self.name} already exists.")
            db.close()
            return
        cur = db.get_cursor()
        cur.execute('INSERT INTO habits (name, periodicity, created_at, streak, last_updated_at) VALUES (?, ?, ?, ?, ?)', 
                    (self.name.title(), self.periodicity, self.created_at.isoformat(), self.streak, self.last_updated_at.isoformat()))
        db.conn.commit()
        cur.close()
        db.close()
        print(f"Created habit {self.name} with periodicity {self.periodicity}")

    def delete_habit(self):
        db = Database()
        cur = db.get_cursor()
        cur.execute('DELETE FROM habits WHERE name = ?', (self.name,))
        db.conn.commit()
        cur.close()
        db.close()
        print(f"Deleted habit {self.name}")

    def mark_habit_as_completed(self):
        db = Database()
        cur = db.get_cursor()
        cur.execute('UPDATE habits SET streak = streak + 1, last_updated_at = ? WHERE name = ?', 
                    (datetime.now().isoformat(), self.name))
        db.conn.commit()
        cur.close()
        db.close()
        print(f"Checked off habit {self.name}")

    def get_all_habits(self):
        db = Database()
        cur = db.get_cursor()
        cur.execute('SELECT * FROM habits')
        habits = cur.fetchall()
        cur.close()
        db.close()
        formatted_habits = [(name, self._format_periodicity(periodicity), created_at.split('T')[0], streak, last_updated_at.split('T')[0]) for name, periodicity, created_at, streak, last_updated_at in habits]
        return formatted_habits

    def longest_daily_streak(self):
        return self._longest_streak('D')
    
    def longest_weekly_streak(self):
        return self._longest_streak('W')
    
    def longest_monthly_streak(self):
        return self._longest_streak('M')

    def _longest_streak(self, periodicity):
        db = Database()
        cur = db.get_cursor()
        cur.execute('SELECT name, MAX(streak) FROM habits WHERE periodicity = ?', (periodicity,))
        longest_streak = cur.fetchall()
        cur.close()
        db.close()
        return longest_streak

    def _format_periodicity(self, periodicity):
        return {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly'}.get(periodicity, periodicity)
