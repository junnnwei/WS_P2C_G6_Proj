import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Define model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ML/Model/detection_model.pkl")

# Load the model once at startup
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    if not isinstance(model, RandomForestClassifier):
        raise TypeError(f"Error: Loaded model is of type {type(model)}, expected RandomForestClassifier")
else:
    raise FileNotFoundError(f"Error: Model file not found at {MODEL_PATH}")

# Scaling factors (unchanged)
scaling_factors = {
    'totalTimeSpentOnPage': 3.25,
    'averageTimePerField': 3.25,
    'mousespeed_sd': 3.0,
    'keystroke_sd': 5.0
}

# Function to classify user agent
def classify_user_agent(user_agent):
    user_agent = user_agent.lower()
    bot_keywords = ['bot', 'spider', 'slurp', 'crawler', 'curl', 'wget']
    return 1 if any(keyword in user_agent for keyword in bot_keywords) else 0

# Features used in training
columns_to_keep = ['totalTimeSpentOnPage', 'averageTimePerField',
                   'mousespeed_sd', 'keystroke_sd', 'user_agent_label']

# Bot detection function
def predictBot(userData):
    try:
        # Convert user data into a DataFrame
        user_df = pd.DataFrame([userData])

        # Convert user agent to label
        user_df['user_agent_label'] = classify_user_agent(userData['user_agent'])

        # Apply scaling factors
        for feature, factor in scaling_factors.items():
            if feature in user_df.columns:
                user_df[feature] *= factor

        # Ensure feature columns match model input
        user_df = user_df.reindex(columns=columns_to_keep, fill_value=0)

        # Ensure model supports `predict_proba`
        if hasattr(model, "predict_proba"):
            bot_Prediction = model.predict_proba(user_df)[:, 1][0]
        else:
            raise AttributeError("Error: Model does not support predict_proba")

        # Force probability to 100% if user-agent is a known bot
        if user_df['user_agent_label'][0] == 1:
            bot_Prediction = 1.0

        return round(bot_Prediction * 100)

    except Exception as e:
        print(f"Error in predictBot: {e}")
        return 0  # Return 0% probability on failure
