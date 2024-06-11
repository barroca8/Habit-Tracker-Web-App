import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('habits.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id UUID,
                name TEXT, 
                periodicity TEXT, 
                created_at TEXT, 
                streak INTEGER, 
                last_updated_at DATE,
                PRIMARY KEY (id)
                )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS habit_tracking (
                habit_id UUID,
                marked_date DATE
            )
            """
        )
        self.conn.commit()
        self.cur.close()

    def get_cursor(self):
        return self.conn.cursor()
    
    def habit_exists(self, habit_id):
        cur = self.get_cursor()
        cur.execute(f"SELECT 1 FROM habits WHERE id = '{str(habit_id)}'")
        row = cur.fetchone()
        cur.close()
        return row is not None

    def close(self):
        self.conn.close()

    def clear_habits_table(self):
        cur = self.get_cursor()
        cur.execute('DROP TABLE IF EXISTS habits')
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id UUID,
                name TEXT, 
                periodicity TEXT, 
                created_at TEXT, 
                streak INTEGER, 
                last_updated_at DATE,
                PRIMARY KEY (id)
                )
            """
        )
        cur.execute('DROP TABLE IF EXISTS habit_tracking')
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS habit_tracking (
                habit_id UUID,
                marked_date DATE
            )
            """
        )
        self.conn.commit()
        cur.close()