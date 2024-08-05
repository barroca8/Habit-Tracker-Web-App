import sqlite3

class Database:
    """
    A class to represent a database connection.
    Methods:
        get_cursor: Get a new database cursor.
        habit_exists: Check if a habit exists by name.
        close: Close the database connection.
        clear_habits_table: Clear the habits and habit tracking tables.
    """

    def __init__(self):
        """Initialize the database connection and create tables if they do not exist."""
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
        """Get a new database cursor."""
        return self.conn.cursor()
    
    def habit_exists(self, habit_name):
        """
        Check if a habit exists by name.

        Parameters:
        habit_name (str): The name of the habit.

        Returns:
        bool: True if the habit exists, False otherwise.
        """
        cur = self.get_cursor()
        cur.execute("SELECT 1 FROM habits WHERE name = ?", (habit_name,))
        row = cur.fetchone()
        cur.close()
        return row is not None

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def clear_habits_table(self):
        """Clear the habits and habit tracking tables."""
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
