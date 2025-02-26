import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your_secret_key")
    MY_EMAIL = "your_email"
    PASSWORD = "your_password"
    DB_NAME = "tasks.db"


