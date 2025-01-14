import sqlite3
import time
import pytz
from datetime import datetime, timedelta
from config import Config
from models import Task
from email_service import EmailService

class TaskScheduler:
    def __init__(self):
        self.email_service = EmailService()

    def get_tasks(self):
        conn = sqlite3.connect(Config.DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, email, class_name, class_days, user_timezone, class_time, class_professor, class_location, last_sent_date FROM tasks')
        tasks = c.fetchall()
        conn.close()
        return tasks

    def update_last_sent_date(self, task_id, date_sent):
        try:
            with sqlite3.connect(Config.DB_NAME) as conn:
                c = conn.cursor()
                c.execute('UPDATE tasks SET last_sent_date = ? WHERE id = ?', (date_sent, task_id))
                conn.commit()
        except Exception as e:
            print(f"Error updating last_sent_date for task {task_id}: {e}")

    def send_task_reminder(self, task):
        self.email_service.send_email(task.email, task)

    def schedule_email(self):
        """Runs once per day and processes reminders accordingly."""
        now_utc = datetime.now(pytz.utc)
        today_str = str(now_utc.date())
        current_day = now_utc.weekday()

        tasks = self.get_tasks()

        for task_data in tasks:
            task = Task(
                id=task_data[0],
                email=task_data[1],
                class_name=task_data[2],
                class_days=task_data[3],
                user_timezone=task_data[4],
                class_time=task_data[5],
                class_professor=task_data[6],
                class_location=task_data[7],
                last_sent_date=task_data[8]
            )

            task_days = list(map(int, task.class_days.split(",")))
            task_time = datetime.strptime(task.class_time, "%H:%M").time()

            user_tz = pytz.timezone(task.user_timezone)
            now_user_tz = now_utc.astimezone(user_tz)
            notify_time = (datetime.combine(now_user_tz.date(), task_time) - timedelta(minutes=15)).time()

            if current_day in task_days and now_user_tz.time() >= notify_time:
                if task.last_sent_date == today_str:
                    print(f"Task reminder for {task.email} already sent today.")
                else:
                    self.send_task_reminder(task)
                    self.update_last_sent_date(task.id, today_str)
                    print(f"Email sent to {task.email}.")

        print("Email scheduling run completed.")









