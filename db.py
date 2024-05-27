import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('habits.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS habits (name TEXT, periodicity TEXT, created_at TEXT, streak INTEGER, last_updated_at DATE)')
        self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor()
    
    def habit_exists(self, habit_name):
        cur = self.get_cursor()
        cur.execute('SELECT 1 FROM habits WHERE name = ?', (habit_name,))
        row = cur.fetchone()
        cur.close()
        return row is not None

    def close(self):
        self.conn.close()

    def clear_habits_table(self):
        cur = self.get_cursor()
        cur.execute('DROP TABLE IF EXISTS habits')
        cur.execute('CREATE TABLE IF NOT EXISTS habits (name TEXT, periodicity TEXT, created_at TEXT, streak INTEGER, last_updated_at DATE)')
        self.conn.commit()
        cur.close()