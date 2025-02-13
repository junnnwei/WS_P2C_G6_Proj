from calendar import day_abbr

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# Load datasets
human_data = pd.read_csv('../ML/datasets/human_training_dataset_synthetic.csv')
bot_data = pd.read_csv('../ML/datasets/bot_training_dataset.csv')

# Add labels: 0 for humans, 1 for bots
human_data['label'] = 0
bot_data['label'] = 1

# print(human_data.dtypes)
# print(bot_data.dtypes)

# Check for invalid entries
# print("Human Data")
# print(human_data[['totalTimeSpentOnPage', 'averageTimePerField', 'mousespeed_sd', 'keystroke_sd']].describe())
#
# print("Bot Data")
# print(bot_data[['totalTimeSpentOnPage', 'averageTimePerField', 'mousespeed_sd', 'keystroke_sd']].describe())

# Reset index after filtering
human_data = human_data.reset_index(drop=True)
# pd.set_option('display.float_format', '{:.2f}'.format)
# print(human_data[['totalTimeSpentOnPage', 'averageTimePerField', 'mousespeed_sd', 'keystroke_sd']].describe())

data = pd.concat([human_data, bot_data], ignore_index=True)
# print(data.head())
# print(data.columns)


# Convert user agent str to labels | identified by keywords
def classify_user_agent(user_agent):
    user_agent = user_agent.lower()
    bot_keywords = ['bot', 'spider', 'slurp', 'crawler', 'agent']
    if any(keyword in user_agent for keyword in bot_keywords):
        return 1
    return 0

data['user_agent_label'] = data['user_agent'].apply(classify_user_agent)

# Weights for feature engineering. Adjust if needed
scaling_factors = {
    'totalTimeSpentOnPage': 0.1,
    'averageTimePerField': 9.0,
    # 'user_agent_label': 0.1,      // I'll introduce this at a later timing
    'browser_width': 0.025,
    'browser_height': 0.025,
    'mousespeed_sd': 20.0,
    'keystroke_sd': 20.0
}

for feature, factor in scaling_factors.items():
    if feature in data.columns:
        data[feature] *= factor

# Only keep required stuff in df
columns_to_keep = ['totalKeyInputs', 'totalTimeSpentOnPage', 'averageTimePerField',
                   'browser_width', 'browser_height', 'mousespeed_sd', 'keystroke_sd', 'label']


data = data[columns_to_keep]

# Separate features and labels
X = data.drop(columns=['label'])
y = data['label']

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest model
rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate model
y_pred = rf_model.predict(X_val)
y_pred_proba = rf_model.predict_proba(X_val)[:, 1]

# Calculate evaluation metrics
accuracy = accuracy_score(y_val, y_pred)
precision = precision_score(y_val, y_pred, pos_label=1)
recall = recall_score(y_val, y_pred, pos_label=1)
f1 = f1_score(y_val, y_pred, pos_label=1)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print("\nClassification Report:\n", classification_report(y_val, y_pred))

# Load test dataset
test_data = pd.read_csv('../ML/datasets/test_dataset.csv')

# Only keep required columns (exclude 'label' from the test data)
test_data = test_data[columns_to_keep[:-1]]  # Exclude 'label' from the test data

# Apply scaling factors to the test data (same as training data scaling)
for feature, factor in scaling_factors.items():
    if feature in test_data.columns:
        test_data[feature] *= factor

# Reindex test data columns to match training data columns
test_data = test_data.reindex(columns=X.columns, fill_value=0)

# Predict on test data
test_predictions_proba = rf_model.predict_proba(test_data)[:, 1]  # Probability of being a bot

# View importance of each feature
feature_importances = pd.DataFrame(rf_model.feature_importances_,
                                   index=X_train.columns,
                                   columns=["Importance"]).sort_values("Importance", ascending=False)

print(feature_importances)

# Save prediction results
output = pd.DataFrame({'Bot_Probability': test_predictions_proba})
output.to_csv('../ML/datasets/ML_predictions.csv', index=False)
print("Predictions saved to ML_predictions.csv.")
