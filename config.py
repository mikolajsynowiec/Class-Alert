import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your_secret_key")
    MY_EMAIL = "mikosyn02@gmail.com"
    PASSWORD = "jkuwhadmocplzfpk"
    DB_NAME = "tasks.db"


