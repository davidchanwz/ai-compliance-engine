from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, func
from app.dependencies import get_db
from app.database.alembic_models import CheckedTransactions  # Assuming this model is defined
import joblib
import numpy as np
import xgboost as xgb
from app.ai_models.interact_with_blockchain import obtain_parameters

# Load the saved model
loaded_model = joblib.load('app/ai_models/fraud_model_v2.pkl')

# Feature expected by the model
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

def predict_anomaly(transaction_id: str, db: Session = Depends(get_db)):
    # Check if the transaction has already been processed
    existing_record = db.execute(
        select(CheckedTransactions)
        .where(CheckedTransactions.transaction_hash == transaction_id)
    ).scalar_one_or_none()

    if existing_record:
        return {
            "transaction_hash": transaction_id,
            "anomaly_rating": existing_record.anomaly_rating,
            "anomaly": existing_record.anomaly,
            "message": "Transaction already checked"
        }

    # Fetch transaction parameters from blockchain
    try:
        params = obtain_parameters(transaction_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch parameters: {str(e)}")

    params = [1.0] + params  # Add the "Unnamed: 0" column value
    new_data = np.array([params])

    # Validate and clean the input data
    if np.any(np.isinf(new_data)):
        new_data = np.where(np.isinf(new_data), np.finfo(np.float32).max, new_data)

    if np.any(np.isnan(new_data)):
        new_data = np.nan_to_num(new_data, nan=0.0)

    threshold = 1e6  # Define a reasonable threshold
    if np.any(np.abs(new_data) > threshold):
        new_data = np.clip(new_data, -threshold, threshold)

    # Convert the input to a DMatrix with feature names
    dnew_data = xgb.DMatrix(new_data, feature_names=feature_names)

    # Predict anomaly rating
    try:
        prediction = loaded_model.predict(dnew_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(e)}")

    anomaly_rating = float(prediction[0])
    binary_prediction = int(anomaly_rating > 0.5)

    # Store the result in the database
    new_record = CheckedTransactions(
        transaction_hash=transaction_id,
        anomaly_rating=anomaly_rating,
        anomaly=binary_prediction,
        checked_at=func.now()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "transaction_hash": transaction_id,
        "anomaly_rating": anomaly_rating,
        "anomaly": binary_prediction,
        "message": "Transaction processed successfully"
    }
