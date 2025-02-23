import sys
import os

# Append only if not already in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)


from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS

from ML.ML_training import predictBot
import math, csv, json, os

app = Flask(__name__, static_folder="../static", template_folder="../templates")

# Allow both localhost and 127.0.0.1 origins
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]}})

@app.route('/')
def default():
    return render_template('login.html')
@app.route('/feedback')
def feedback2():
    return render_template('feedback.html')

@app.route('/login')
def login2():
    return render_template('login.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route("/model")
def model_page():
    return render_template("model.html") 

@app.route("/captcha_templates/<filename>")
def captcha_template(filename):
    return send_from_directory("/captcha_templates", filename)

@app.route('/api/detect_bot', methods=['POST'])
def detect_bot():
    user_data = request.get_json()
    bot_probability = predictBot(user_data)
    
    if bot_probability < 30:
        captcha_level = "easy"
    elif 30 <= bot_probability < 60:
        captcha_level = "medium"
    elif 60 <= bot_probability < 90:
        captcha_level = "hard"
    elif bot_probability >= 95:
        captcha_level = "blocked"

    return jsonify({
        "bot_probability": bot_probability,
        "captcha_level": captcha_level
    })

# Backend metric processing
def calculateKeystrokeSD(interval_data):
    if len(interval_data) == 0:
        return 0.0

    mean = sum(interval_data) / len(interval_data)
    variance = sum([(x - mean) ** 2 for x in interval_data]) / len(interval_data)
    return math.sqrt(variance)

def calc_keystroke_std_dev(data):
    keystroke_intervals = data.get('keyPressIntervals', [])

    keystroke_std_dev = calculateKeystrokeSD(keystroke_intervals)
    return keystroke_std_dev
    
# Mouse: Speed
def parse_movement_data(movement_data):
    parsed_data = []
    for entry in movement_data:
        parts = entry.split('-')
        action = parts[0]
        x, y, timestamp = map(int, parts[1:])
        parsed_data.append((action, x, y, timestamp))
    return parsed_data

def calculate_speed(data):
    speeds = []
    for i in range(1, len(data)):
        x1, y1, t1 = data[i - 1][1:]
        x2, y2, t2 = data[i][1:]
        
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        time_diff = (t2 - t1) / 1000  # Convert ms to seconds
        
        if time_diff > 0:
            speed = distance / time_diff
        else:
            speed = 0
        
        speeds.append(speed)
    return speeds


def calculate_standard_deviation(speeds):
    """ Computes the standard deviation of the speed values. """
    if len(speeds) < 2:
        return 0  # Not enough data to compute standard deviation

    mean_speed = sum(speeds) / len(speeds)
    variance = sum((speed - mean_speed) ** 2 for speed in speeds) / len(speeds)
    return math.sqrt(variance)


# Write to CSV for data collection
def append_to_csv(response):
    # Note: AMEND TO YOUR OWN FILE NAMES TO COLLECT DATA SEPARATELY
    csv_directory = 'data_collection'
    csv_file_path = os.path.join(csv_directory, 'jw_bot_data_collection.csv')


    # Ensure the directory exists, if not create it
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    csv_header = ['sessionID', 'formId', 'totalKeyInputs', 'totalTimeSpentOnPage', 'averageTimePerField', 'browser_width', 'browser_height',
                  'pixel_ratio', 'user_agent', 'platform', 'language', 'timezone', 'mousespeed_sd', 'keystroke_sd']

    # Prepare the row for CSV by extracting required fields
    row = [
        response.get('sessionID', ''),
        response.get('formId', ''),
        response.get('totalKeyInputs', 0),
        response.get('totalTimeSpentOnPage', 0),
        response.get('averageTimePerField', 0),
        response.get('browser_width', ''),
        response.get('browser_height', ''),
        response.get('pixelRatio', ''),
        response.get('user_agent', ''),
        response.get('platform', ''),
        response.get('language', ''),
        response.get('timezone', ''),
        response.get('mousespeed_sd', 0),
        response.get('keystroke_sd', 0),
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
        # print("Received metrics:", data)
        
        # Extract movement data
        movement_data = data.get("movementData", [])
        parsed_data = parse_movement_data(movement_data[1:16]) if movement_data else []
        speeds = calculate_speed(parsed_data) if parsed_data else []
        speed_std_dev = calculate_standard_deviation(speeds) if speeds else 0  # Standard deviation
        keystroke_std_dev = calc_keystroke_std_dev(data)
        
        response = {
            "sessionID": data.get("sessionID"),
            "formId": data.get("formId"),
            "totalKeyInputs": data.get("totalKeyInputs", 0),
            "totalTimeSpentOnPage": data.get("totalTimeSpentOnPage", 0),
            "averageTimePerField": data.get("averageTimePerField", 0),
            "browser_width": data.get("width"),
            "browser_height": data.get("height"),
            "pixelRatio": data.get("pixelRatio"),
            "user_agent": data.get("userAgent"),
            "platform": data.get("platform"),
            "language": data.get("language"),
            "timezone": data.get("timezone"),
            "fieldInteractions": data.get("fieldInteractions",{}),
            "speeds": speeds,
            "keyPressIntervals": data.get("keyPressIntervals"),
            "mousespeed_sd": speed_std_dev,
            "keystroke_sd": keystroke_std_dev
        }

        print("Processed Metrics:", response)

        # Note: ONLY include this line when attempting to collect data (TO BE REMOVED POST-DATA COLLECTION)
        append_to_csv(response)
        return jsonify(response), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)