import sqlite3
from config import Config

class Task:
    def __init__(self, email, class_name, class_days, user_timezone, class_time, class_professor, class_location, id=None, last_sent_date=None):
        self.id = id
        self.email = email
        self.class_name = class_name
        self.class_days = class_days
        self.user_timezone = user_timezone
        self.class_time = class_time
        self.class_professor = class_professor
        self.class_location = class_location
        self.last_sent_date = last_sent_date  # Defaults to None for new tasks

    @staticmethod
    def create_db():
        conn = sqlite3.connect(Config.DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        class_name TEXT,
                        class_days TEXT,
                        user_timezone TEXT,
                        class_time TEXT,
                        class_professor TEXT,
                        class_location TEXT,
                        last_sent_date TEXT)''')
        conn.commit()
        conn.close()

    @staticmethod
    def save_task(task, scheduler):
        try:
            conn = sqlite3.connect(Config.DB_NAME)
            c = conn.cursor()
            # Check for duplicates
            c.execute('''SELECT * FROM tasks 
                             WHERE email = ? AND class_name = ? AND class_time = ? AND class_days = ?''',
                      (task.email, task.class_name, task.class_time, task.class_days))
            existing_task = c.fetchone()
            if existing_task:
                conn.close()
                return False  # Duplicate found; do not save

            # Insert the new task
            c.execute('''INSERT INTO tasks (email, class_name, class_days, user_timezone, class_time,
                                                class_professor, class_location, last_sent_date) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (task.email, task.class_name, task.class_days, task.user_timezone, task.class_time,
                       task.class_professor, task.class_location, None))
            conn.commit()
            conn.close()

            # **Run the scheduler function immediately after adding a task**
            scheduler.schedule_email()

            print(f"Task successfully created and scheduler executed!")
            return True
        except Exception as e:
            print(f"Error saving task: {e}")
            return False

    @staticmethod
    def check_existing_task(email, class_name, class_time, class_days):
        conn = sqlite3.connect(Config.DB_NAME)
        c = conn.cursor()
        c.execute('''SELECT * FROM tasks 
                     WHERE email = ? AND class_name = ? AND class_time = ? AND class_days = ?''',
                  (email, class_name, class_time, class_days))
        existing_task = c.fetchone()
        conn.close()
        return existing_task is not None
