import joblib
import numpy as np
import xgboost as xgb
from interact_with_blockchain import obtain_parameters
from sqlalchemy import create_engine, MetaData, Table, insert, select, func
import os

# Load the saved model
loaded_model = joblib.load('app/ai_models/fraud_model_v2.pkl')
print("Model loaded successfully")

# Database credentials from environment variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Define the required table from the database
engine = create_engine(DATABASE_URL)
metadata = MetaData()
changes_table = Table("Checked_transactions", metadata, autoload_with=engine)

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

def predict_anomaly(transaction_id):
    # Connect to supabase
    with engine.connect() as connection:
        result = connection.execute(
                    select(changes_table.c.anomaly_rating, changes_table.c.anomaly) 
                    .where(changes_table.c.transaction_hash == transaction_id) 
                ).fetchone()

    # If transaction has been checked before
    if result:
        anomaly_rating = result[0]
        anomaly = result[1]
        print(f"Anomaly Rating: {anomaly_rating}")
        print(f"Binary Prediction: {anomaly}")

    else:
        params = obtain_parameters(transaction_id)
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
        print(f"Input shape: {new_data.shape}")

        prediction = loaded_model.predict(dnew_data)
        print(f"Anomaly Rating: {prediction}")

        threshold = 0.5
        binary_prediction = int(prediction[0] > threshold)
        print(f"Binary Prediction: {binary_prediction}")


        anomaly_rating = float(prediction[0]) 

        # Store values into the Checked_transactions table for future reference 
        with engine.connect() as connection:
            connection.execute(insert(changes_table).values({
                "transaction_hash": transaction_id,
                "anomaly_rating": anomaly_rating,
                "anomaly": binary_prediction,
                "checked_at": func.now() 
            }))
            connection.commit()

if __name__ == "__main__":
    transaction_id = '0xd4430d219af3f5b2ade7cfee82fa17b893e51d4c5015b5f7406841790ea63e37'
    predict_anomaly(transaction_id)
