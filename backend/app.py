from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import math, csv, json, os
app = Flask(__name__, static_folder="../static", template_folder="../templates")

# Allow both localhost and 127.0.0.1 origins
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]}})

# Login page
@app.route('/')
def login():
    return render_template('login.html')

# Signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Feedback page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Backend metric processing
def calculateKeystrokeSD(interval_data):
    if len(interval_data) == 0:
        return 0

    mean = sum(interval_data) / len(interval_data)
    variance = sum([(x - mean) ** 2 for x in interval_data]) / len(interval_data)
    return math.sqrt(variance)

def recalculateMetrics(data):
    keystroke_intervals = data.get('keyPressIntervals', [])

    std_dev = calculateKeystrokeSD(keystroke_intervals)
    data['keystroke_sd'] = std_dev

def append_to_csv(data):
    # Note: AMEND TO YOUR OWN FILE NAMES TO COLLECT DATA SEPARATELY
    csv_directory = 'data_collection'
    csv_file_path = os.path.join(csv_directory, 'jw_data_collection.csv')

    # Ensure the directory exists, if not create it
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    csv_header = ['sessionID', 'formId', 'totalKeyInputs', 'totalTimeSpentOnPage', 'browser_width', 'browser_height',
                  'pixel_ratio', 'user_agent', 'platform', 'language', 'timezone', 'mousespeed_sd', 'keystroke_sd']

    # Prepare the row for CSV by extracting required fields
    row = [
        data.get('sessionID', ''),
        data.get('formId', ''),
        data.get('totalKeyInputs', 0),
        data.get('totalTimeSpentOnPage', 0),
        data.get('width', ''),
        data.get('height', ''),
        data.get('pixelRatio', ''),
        data.get('userAgent', ''),
        data.get('platform', ''),
        data.get('language', ''),
        data.get('timezone', ''),
        data.get('mousespeed_sd', 0),
        data.get('keystroke_sd', 0),
    ]

    # Check if the file exists
    file_exists = os.path.isfile(csv_file_path)

    # Open CSV file in append mode
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(csv_header)

        writer.writerow(row)

# API
@app.route('/api/analysis-metrics', methods=['POST'])
def analysis_metrics():
    try:
        data = request.get_json()
        print("Received metrics:", data)

        recalculateMetrics(data)

        print("\nCalculated metrics:", data)

        # Note: ONLY include this line when attempting to collect data (TO BE REMOVED POST-DATA COLLECTION)
        append_to_csv(data)

        return jsonify({"status": "success", "message": "Metrics received!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)