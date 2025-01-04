import pandas as pd
import numpy as np

# Feature names as per the model's expectations
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

# Generate 100 rows of synthetic data
np.random.seed(42)  # For reproducibility
data = {
    'Unnamed: 0': np.arange(1, 101),  # Unique identifier
    'Avg min between sent tnx': np.random.uniform(500, 1000, 100),
    'Avg min between received tnx': np.random.uniform(1000, 2000, 100),
    'Time Diff between first and last (Mins)': np.random.uniform(100000, 500000, 100),
    'Sent tnx': np.random.randint(100, 1000, 100),
    'Received Tnx': np.random.randint(50, 500, 100),
    'Number of Created Contracts': np.random.randint(0, 10, 100),
    'max value received ': np.random.uniform(1, 100, 100),
    'avg val received': np.random.uniform(0.1, 50, 100),
    'avg val sent': np.random.uniform(0.1, 50, 100),
    'total Ether sent': np.random.uniform(1, 1000, 100),
    'total ether balance': np.random.uniform(-500, 500, 100),
    ' ERC20 total Ether received': np.random.uniform(1000, 1000000, 100),
    ' ERC20 total ether sent': np.random.uniform(1000, 1000000, 100),
    ' ERC20 total Ether sent contract': np.random.uniform(0, 500000, 100),
    ' ERC20 uniq sent addr': np.random.randint(1, 100, 100),
    ' ERC20 uniq rec token name': np.random.randint(1, 100, 100),
    ' ERC20 most sent token type': np.random.uniform(1, 100, 100),
    ' ERC20_most_rec_token_type': np.random.uniform(1, 100, 100)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
file_name = 'datasets/test_data_100_rows.csv'
df.to_csv(file_name, index=False)
print(f"Test data saved to {file_name}")