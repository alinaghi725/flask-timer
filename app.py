from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = 'timers.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_timer', methods=['POST'])
def save_timer():
    data = request.json
    name = data.get('name')
    duration = data.get('duration')

    if not name or not duration:
        return jsonify({'status': 'error', 'message': 'Name and duration required'}), 400

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Name', 'Duration'])
        writer.writerow([name, duration])

    return jsonify({'status': 'success', 'message': 'Timer saved'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
