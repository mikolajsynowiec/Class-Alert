# Class Reminder App

A Python-based tool to send email reminders for scheduled classes. Features include multi-threading, time zone management, and JSON-based persistent data storage.

## Features
- Sends email notifications 15 minutes before scheduled classes.
- Handles time zones using `pytz`.
- Validates user inputs for days, times, and email.
- Stores and manages task data in a `scheduled_tasks.json` file.
- Automates the email reminder process when hosted on PythonAnywhere.
- 
## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/class-reminder.git
   
2.Install the required dependencies
pip install -r requirements.txt

3. Set up your email credentials in the script.

4. For PythonAnywhere Hosting:
Upload the project files to your PythonAnywhere account.
Set up the required cron job to run the script at intervals (e.g., every minute) to send notifications.
Ensure that your PythonAnywhere account supports email sending (you may need to configure a Gmail account or another SMTP service).

5. Run the app:
   python app.py

Requirements
Python 3.8+
Libraries: pytz, smtplib

### Notes:
- Hosting on **PythonAnywhere** ensures the app will run continuously in the cloud, sending automated emails to users based on their scheduled class times.
- You may need to configure **SMTP settings** and **cron jobs** to automate the execution of the Python script on PythonAnywhere.

Let me know if you need more details on the PythonAnywhere setup!
