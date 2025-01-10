from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from datetime import timedelta
from app.core.jwt import create_access_token

client = TestClient(app)

# Test Case 1: /audit-trail Endpoint
def test_create_audit_log():
    # Step 1: Create a valid JWT token for authentication
    data = {"sub": "user_123"}
    token = create_access_token(data)
    
    # Step 2: Simulate POST request to /transaction-check endpoint to trigger audit log creation
    with patch('app.audit_trail.add_audit_log') as mock_add_audit_log:
        mock_add_audit_log.return_value = {"timestamp": "2025-01-10T12:00:00", "user_id": "user_123", "action": "Created", "details": "Created audit entry"}
        response = client.post(
            '/audit-trail',
            json={"transaction_hash": "valid_hash_123", "action": "Created", "details": "Created audit entry"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert "timestamp" in response.json()
        assert response.json()["user_id"] == "user_123"
        assert response.json()["action"] == "Created"

# Test Case 2: /authentication Endpoint (Login)
def test_user_login():
    # Step 1: Simulate POST request to login endpoint with valid credentials
    response = client.post('/authentication/login', json={"email": "user@example.com", "password": "password123"})
    
    # Step 2: Check response for successful login and token generation
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Step 3: Verify the access token is valid by decoding it
    token = response.json()["access_token"]
    decoded_data = create_access_token.verify_access_token(token)
    assert decoded_data["sub"] == "user@example.com"  # Assuming sub is email

# Test Case 3: /transaction-check Endpoint
def test_transaction_check():
    # Step 1: Create a valid JWT token for authentication
    data = {"sub": "user_123"}
    token = create_access_token(data)

    # Step 2: Mock blockchain data and anomaly prediction response
    with patch('app.transaction_check.get_transaction_data', return_value={'status': 'success', 'value': 1000}), \
         patch('app.transaction_check.predict_anomaly', return_value=0.1):  # Low anomaly score
        response = client.post(
            '/transaction-check',
            json={"transaction_hash": "valid_hash_123"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Step 3: Assert response status and expected output
        assert response.status_code == 200
        assert "anomaly_score" in response.json()
        assert response.json()["anomaly_score"] == 0.1  # Assuming a score between 0 and 1