def test_transaction_check_compliant(test_client):
    response = test_client.post(
        "/compliance/transaction-check",
        json={
            "transaction_id": "txn_123",
            "amount": 500.0,
            "sender_account": "sender123",
            "receiver_account": "receiver456",
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "transaction_id": "txn_123",
        "is_compliant": True,
        "risk_score": 0.1,
    }

def test_transaction_check_non_compliant(test_client):
    response = test_client.post(
        "/compliance/transaction-check",
        json={
            "transaction_id": "txn_456",
            "amount": 5000.0,
            "sender_account": "sender789",
            "receiver_account": "receiver123",
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "transaction_id": "txn_456",
        "is_compliant": False,
        "risk_score": 0.8,
    }