import re
import json
from datetime import datetime, timedelta, timezone
import smtplib
import time
import threading
import pytz

my_email = "your_gmail"
password = "your_password"

def days_to_names(days_str):
    day_mapping = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    days = list(map(int, days_str.split(',')))
    return ", ".join(day_mapping[day] for day in days)


def convert_to_utc(local_time_str, local_timezone_str):
    try:
        # Parse the local time
        local_time = datetime.strptime(local_time_str, "%H:%M")
        local_tz = pytz.timezone(local_timezone_str)

        # Localize the time considering DST
        today_date = datetime.now().date()
        localized_time = local_tz.localize(datetime.combine(today_date, local_time.time()), is_dst=None)

        # Convert to UTC
        utc_time = localized_time.astimezone(pytz.utc)

        return utc_time.strftime("%H:%M")

    except Exception as e:
        print(f"Error in convert_to_utc: {e}")
        return None


def convert_to_local_time(utc_time_str, user_timezone):
    try:
        # Parse UTC time
        utc_time = datetime.strptime(utc_time_str, "%H:%M").replace(tzinfo=timezone.utc)
        local_tz = pytz.timezone(user_timezone)

        # Convert to local timezone
        local_time = utc_time.astimezone(local_tz)

        # Handle DST correctly
        if local_tz.dst(local_time) is not None:
            local_time += local_tz.dst(local_time)

        # Subtract 4 minutes to match the input time
        local_time -= timedelta(minutes=4)

        return local_time.strftime("%H:%M")

    except Exception as e:
        print(f"Error in convert_to_local_time: {e}")
        return None


def send_email(email, new_data):
    try:
        user_timezone = new_data['user_timezone']

        # Ensure the local time is displayed correctly
        local_class_time = convert_to_local_time(new_data['class_time'], user_timezone)

        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            formatted_data = f"""
            Email: {new_data['email']}
            Class Name: {new_data['class_name']}
            Class Days: {days_to_names(new_data['class_days'])}
            Class Time: {local_class_time} (local time)  # This will now match input time
            Professor: {new_data['class_professor']}
            Location: {new_data['class_location']}
            """
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email,
                msg=f"Subject: Hey! You have class in 15 min!\n\n{formatted_data}"
            )
        print(f"Email sent to {email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def save_task_to_file(task):
    # Check if the file exists and is not empty
    try:
        with open("scheduled_tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []  # If the file doesn't exist, start with an empty list
    except json.JSONDecodeError:
        tasks = []  # If the file is empty or corrupted, reset to an empty list

    # Append the new task to the list
    tasks.append(task)

    # Write the updated list of tasks back to the file
    with open("scheduled_tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    # Debug print to check what's being saved
    print(f"Saving task: {task}")

def is_valid_time_format(time_str):
    return re.match(r'^\d{2}:\d{2}$', time_str) and int(time_str[:2]) < 24 and int(time_str[3:]) < 60

def is_valid_days_format(days_str):
    try:
        days = list(map(int, days_str.split(',')))
        return all(0 <= day <= 6 for day in days) and len(set(days)) <= 7
    except ValueError:
        return False

def schedule_email():
    while True:
        now_utc = datetime.now(timezone.utc)
        current_day = now_utc.weekday()

        try:
            # Open the JSON file and handle empty or non-existent file gracefully
            try:
                with open("scheduled_tasks.json", "r") as file:
                    tasks = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                tasks = []  # Initialize an empty list if file is empty or not found

            tasks_to_save = []
            for task in tasks:
                task_days = list(map(int, task["class_days"].split(",")))
                last_sent_date = task.get("last_sent_date")
                task_time = datetime.strptime(task["class_time"], "%H:%M").time()

                # Subtract 15 minutes from the class time
                notification_time = (datetime.combine(datetime.today(), task_time) - timedelta(minutes=15)).time()

                if (
                    current_day in task_days
                    and notification_time <= now_utc.time() < task_time
                    and (last_sent_date is None or last_sent_date != str(now_utc.date()))
                ):
                    send_email(task["email"], task)
                    task["last_sent_date"] = str(now_utc.date())
                tasks_to_save.append(task)

            # Save updated tasks back to the file
            with open("scheduled_tasks.json", "w") as file:
                json.dump(tasks_to_save, file, indent=4)
        except Exception as e:
            print(f"Error in schedule_email: {e}")

        time.sleep(60)





def main():
    print("Welcome to Class Alert! Fill out all information about your classes here, and we will send you an email notification!")

    while True:  # Start a loop to allow multiple class entries
        email = input("Enter your email address: ")
        class_name = input("Enter your class name: ")
        class_days = input("Enter your class days as numbers (Monday=0, Sunday=6, separated by commas): ")
        while not is_valid_days_format(class_days):
            print(
                "Invalid days format. Please enter numbers between 0 (Monday) and 6 (Sunday), separated by commas, with a maximum of 7 days.")
            class_days = input("Enter your class days as numbers (Monday=0, Sunday=6, separated by commas): ")

        user_timezone = input("Enter your time zone (e.g., America/New_York, Europe/London): ")
        while user_timezone not in pytz.all_timezones:
            print("Invalid time zone. Please enter a valid time zone (e.g., America/New_York, Europe/London).")
            user_timezone = input("Enter your time zone (e.g., America/New_York, Europe/London): ")

        class_time = input("Enter your class time (HH:MM) in your local time: ")
        while not is_valid_time_format(class_time):
            print("Invalid time format. Please enter in HH:MM format (e.g., 14:30).")
            class_time = input("Enter your class time (HH:MM) in your local time: ")

        utc_class_time = convert_to_utc(class_time, user_timezone)

        class_professor = input("Enter your professor name: ")
        class_location = input("Enter your class location: ")

        task = {
            "email": email,
            "class_name": class_name,
            "class_days": class_days,
            "class_time": utc_class_time,
            "class_professor": class_professor,
            "class_location": class_location,
            "user_timezone": user_timezone  # Add user_timezone here
        }

        save_task_to_file(task)
        print("\nClass schedule saved successfully!")

        add_another = input("\nDo you want to add another class? (y/n): ").strip().lower()
        while add_another not in ["y", "n"]:
            print("Invalid option. Please enter 'y' for yes or 'n' for no.")
            add_another = input("Do you want to add another class? (y/n): ").strip().lower()

        if add_another == "n":  # Exit the loop if the user doesn't want to add more classes
            print("\nAll classes have been added. Scheduler is now running...")
            break


scheduler_thread = threading.Thread(target=schedule_email, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    main()  # Collect schedule information once

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_email, daemon=True)
    scheduler_thread.start()

    # Keep the script running to allow the scheduler to work
    while True:
        time.sleep(60)