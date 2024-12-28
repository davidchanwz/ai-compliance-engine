def test_kyc_verified(test_client):
    response = test_client.post(
        "/kyc/verify",
        json={
            "user_id": "user123",
            "full_name": "John Doe",
            "dob": "1990-01-01",
            "id_number": "A1234567",
            "id_type": "Passport",
        }
    )
    assert response.status_code == 200
    assert response.json() == {"user_id": "user123", "is_verified": True}

def test_kyc_not_verified(test_client):
    response = test_client.post(
        "/kyc/verify",
        json={
            "user_id": "user456",
            "full_name": "Jane Doe",
            "dob": "1995-05-05",
            "id_number": "B7654321",
            "id_type": "Passport",
        }
    )
    assert response.status_code == 200
    assert response.json() == {"user_id": "user456", "is_verified": False}