import joblib
import numpy as np
import xgboost as xgb

# Load the saved model
loaded_model = joblib.load('app/ai_models/fraud_model_v2.pkl')
print("Model loaded successfully")

# Feature names expected by the model
feature_names = [
    'Unnamed: 0', 'Avg min between sent tnx', 'Avg min between received tnx',
    'Time Diff between first and last (Mins)', 'Sent tnx', 'Received Tnx',
    'Number of Created Contracts', 'max value received ', 'avg val received',
    'avg val sent', 'total Ether sent', 'total ether balance',
    ' ERC20 total Ether received', ' ERC20 total ether sent',
    ' ERC20 total Ether sent contract', ' ERC20 uniq sent addr',
    ' ERC20 uniq rec token name', ' ERC20 most sent token type',
    ' ERC20_most_rec_token_type'
]

# Input data aligned with the model's features
new_data = np.array([[
    1.0, 800.0, 1200.0, 500000.0, 600.0, 75.0, 1.0, 50.0, 10.0,
    5.0, 300.0, 200.0, 500000.0, 400000.0, 100000.0, 25.0, 35.0, 1.0e+76, 30.0
]])

# Validate and clean the input data
if np.any(np.isinf(new_data)):
    print("Input contains infinity values. Replacing...")
    new_data = np.where(np.isinf(new_data), np.finfo(np.float32).max, new_data)

if np.any(np.isnan(new_data)):
    print("Input contains NaN values. Replacing...")
    new_data = np.nan_to_num(new_data, nan=0.0)

threshold = 1e6  # Define a reasonable threshold
if np.any(np.abs(new_data) > threshold):
    print("Input contains excessively large values. Capping...")
    new_data = np.clip(new_data, -threshold, threshold)

# Convert the input to a DMatrix with feature names
dnew_data = xgb.DMatrix(new_data, feature_names=feature_names)
print(f"Input shape: {new_data.shape}")

# Make prediction
prediction = loaded_model.predict(dnew_data)
print(f"Prediction: {prediction}")

# Convert probability to binary classification
threshold = 0.5
binary_prediction = int(prediction[0] > threshold)
print(f"Binary Prediction: {binary_prediction}")