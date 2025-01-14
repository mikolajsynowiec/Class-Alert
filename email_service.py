import smtplib
from config import Config

class EmailService:
    @staticmethod
    def send_email(email, task):
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()
                connection.login(user=Config.MY_EMAIL, password=Config.PASSWORD)
                message = (f"Subject: Reminder: {task.class_name} in 15 min!\n\n"
                           f"Class: {task.class_name}\n"
                           f"Time: {task.class_time} (local time)\n"
                           f"Professor: {task.class_professor}\n"
                           f"Location: {task.class_location}\n")
                connection.sendmail(from_addr=Config.MY_EMAIL, to_addrs=email, msg=message)
            print(f"Email sent to {email}.")
        except Exception as e:
            print(f"Failed to send email: {e}")

