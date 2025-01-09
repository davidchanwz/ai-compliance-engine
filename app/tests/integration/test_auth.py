import pytest
from unittest.mock import patch, MagicMock
from app.core.security import get_password_hash
from app.database.alembic_models import User


@patch("app.api.endpoints.auth.get_user_by_email")
def test_login_success(mock_get_user_by_email, test_client):
    # Mock a User object
    user_mock = MagicMock(spec=User)
    user_mock.id = "123e4567-e89b-12d3-a456-426614174000"
    user_mock.email = "test@example.com"
    user_mock.hashed_password = "$2b$12$RhARjF0pbLSDI8HfOVVVcOLAksd0B7nPHHhWIFMzLU84eeyxClVcG"
    user_mock.created_at = "2023-01-01T00:00:00Z"

    mock_get_user_by_email.return_value = user_mock  # Return the mocked User object

    response = test_client.post("/login", json={"email": "test@example.com", "password": "password"})

    # Assertions
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_failure(test_client):
    response = test_client.post("/login", json={"email": "user@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_protected_route_authorized_with_real_user(test_client, create_test_user):
    # 1) Log in with the *real* user
    login_response = test_client.post(
        "/login",
        json={"email": create_test_user.email, "password": "password"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # 2) Access the protected route with real token
    response = test_client.get(
        "/protected",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "message" in response.json()




