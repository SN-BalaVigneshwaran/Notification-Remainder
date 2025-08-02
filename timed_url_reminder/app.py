from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            reminder_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form['url']
    time = request.form['time']  # Time format: 'YYYY-MM-DDTHH:MM' from datetime-local input

    # Convert to datetime string
    reminder_time = datetime.strptime(time, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')

    # Save to DB
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (url, reminder_time) VALUES (?, ?)", (url, reminder_time))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Create table if not exists
    app.run(debug=True)
