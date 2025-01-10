import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Unit Tests for Anomaly Detection

def test_successful_transaction_anomaly_check():
    """
    Test that the endpoint successfully processes a valid transaction hash
    and returns an accurate anomaly rating.
    """
    valid_payload = {
        "transaction_id": "0x09533be63ad3fb86c56fe363562294713578ac110119a71fae3efd03d1d7fe87"
    }
    response = client.post("/transaction-check", json=valid_payload)
    assert response.status_code == 200
    assert "anomalous" in response.json()
    assert "anomaly_score" in response.json()
    assert isinstance(response.json()["anomalous"], bool)
    assert isinstance(response.json()["anomaly_score"], float)

def test_invalid_transaction_hash():
    """
    Test that the endpoint responds with an appropriate error when an
    invalid or malformed transaction hash is provided.
    """
    invalid_payload = {
        "transaction_id": "invalid_hash"
    }
    response = client.post("/transaction-check", json=invalid_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid transaction hash"}

def test_missing_transaction_hash():
    """
    Test that the endpoint responds with a 400 Bad Request error when no
    transaction_id is provided in the request body.
    """
    invalid_payload = {}  # Empty payload
    response = client.post("/transaction-check", json=invalid_payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing transaction_id"}