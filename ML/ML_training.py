import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# Load datasets
human_data = pd.read_csv('./ML/datasets/human_training_dataset.csv')
bot_data = pd.read_csv('./ML/datasets/bot_training_dataset.csv')

# Add labels: 0 for humans, 1 for bots
human_data['label'] = 0
bot_data['label'] = 1

data = pd.concat([human_data, bot_data], ignore_index=True)

# Weights for feature engineering. Adjust if needed
scaling_factors = {
    'totalTimeSpentOnPage': 3.0,
    'averageTimePerField': 3.0,
    'mousespeed_sd': 1.5,
    'keystroke_sd': 3.0
}

for feature, factor in scaling_factors.items():
    if feature in data.columns:
        data[feature] *= factor

# Separate features and labels
X = data.drop(columns=['label'])
y = data['label']

# Handle non-numeric columns with one-hot encoding
X = pd.get_dummies(X)

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
test_data = pd.read_csv('./ML/datasets/test_dataset.csv')

# Add missing columns as zeros and drop extra columns
for col in X.columns:
    if col not in test_data.columns:
        test_data[col] = 0
test_data = test_data[X.columns]

# Predict on test data
test_predictions_proba = rf_model.predict_proba(test_data)[:, 1]  # Probability of being a bot

# Save prediction results
output = pd.DataFrame({'Bot_Probability': test_predictions_proba})
output.to_csv('./ML/datasets/ML_predictions.csv', index=False)
print("Predictions saved to ML_predictions.csv.")
