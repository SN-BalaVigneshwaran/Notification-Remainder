from flask import Flask, render_template, request, jsonify
from datetime import datetime
import threading
import time
import webbrowser

app = Flask(__name__)

# Function to wait until scheduled time and open URL
def schedule_url(open_time, url):
    while True:
        if datetime.now() >= open_time:
            webbrowser.open(url)
            break
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    url = data['url']
    time_str = data['time']  # Format: "YYYY-MM-DDTHH:MM"
    try:
        scheduled_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        threading.Thread(target=schedule_url, args=(scheduled_time, url)).start()
        return jsonify({"message": "Reminder scheduled successfully!"})
    except ValueError:
        return jsonify({"message": "Invalid date/time format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
