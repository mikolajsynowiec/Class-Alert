import threading
from flask import Flask, request, render_template, redirect, url_for, flash
from models import Task
from scheduler import TaskScheduler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Create database if it doesn't exist
Task.create_db()

# Initialize and start the scheduler thread
scheduler = TaskScheduler()
scheduler_thread = threading.Thread(target=scheduler.schedule_email, daemon=True)
scheduler_thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        class_name = request.form["class_name"]
        class_days = request.form["class_days"]
        user_timezone = request.form["timezone"]
        class_time = request.form["class_time"]
        class_professor = request.form["professor"]
        class_location = request.form["location"]

        task = Task(email, class_name, class_days, user_timezone, class_time, class_professor, class_location)

        # **Pass the scheduler instance to save_task()**
        if Task.save_task(task, scheduler):
            flash("Task saved successfully!")
        else:
            flash("Task already exists! No duplicate entries allowed.")

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

