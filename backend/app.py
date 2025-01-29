from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import math, csv, json
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
def calculateKeystrokeSD(internval_data):
    if len(internval_data) == 0:
        return 0

    mean = sum(internval_data) / len(internval_data)
    variance = sum([(x - mean) ** 2 for x in internval_data]) / len(internval_data)
    return math.sqrt(variance)

def recalculateMetrics(data):
    keystroke_intervals = data.get('keyPressIntervals', [])

    std_dev = calculateKeystrokeSD(keystroke_intervals)
    data['keystroke_sd'] = std_dev

# API
@app.route('/api/analysis-metrics', methods=['POST'])
def analysis_metrics():
    try:
        data = request.get_json()
        print("Received metrics:", data)

        recalculateMetrics(data)

        print("\nCalculated metrics:", data)

        # Note: ONLY include this line when attempting to collect data (TO BE REMOVED POST-DATA COLLECTION)
        # append_to_csv(data)

        return jsonify({"status": "success", "message": "Metrics received!"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)