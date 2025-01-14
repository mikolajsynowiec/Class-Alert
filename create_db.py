import sqlite3

# Create SQLite database and table
def create_db():
    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    # Create the tasks table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        class_name TEXT,
        class_days TEXT,
        user_timezone TEXT,
        class_time TEXT,
        class_professor TEXT,
        class_location TEXT,
        last_sent_date TEXT
    )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()

# Run the function to create the database and table
create_db()

print("Database and table created successfully!")
