from flask import Flask, render_template, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

def save_time(username, start_time, end_time):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    duration = end_dt - start_dt
    duration_seconds = int(duration.total_seconds())

    with open('times.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, start_time, end_time, duration_seconds])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    username = data.get('username')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not (username and start_time and end_time):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    save_time(username, start_time, end_time)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

@app.route('/')
def index():
    return app.send_static_file('index.html')  # یا render_template اگر داری استفاده می‌کنی

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # اگر فایل وجود داره، داده‌ها رو می‌خونیم و بهش اضافه می‌کنیم، اگر نه یه لیست خالی درست می‌کنیم
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    else:
        all_data = []

    all_data.append(data)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "success"})
