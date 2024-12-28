def test_valid_login(test_client):
    # Simulate a POST request to /auth/login
    response = test_client.post(
        "/auth/login",
        json={"username": "admin", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json() == {"access_token": "fake-jwt-token", "token_type": "bearer"}

def test_invalid_login(test_client):
    # Simulate a POST request to /auth/login with invalid credentials
    response = test_client.post(
        "/auth/login",
        json={"username": "user", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}