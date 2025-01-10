import pytest
from unittest.mock import patch, MagicMock
from app.database.alembic_models import AuditTrail


@patch("app.api.endpoints.audit_trail.get_current_user")
@patch("app.api.endpoints.audit_trail.get_db")
def test_successful_retrieval_of_audit_logs(mock_get_db, mock_get_current_user, test_client):
    # Mock the authenticated user
    user_mock = MagicMock()
    user_mock.id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_current_user.return_value = user_mock

    # Mock the database query
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    audit_log_mock = AuditTrail(
        id="662e0273-9438-4b87-9d55-51a8d3ec28bc",
        timestamp="2025-01-10T07:53:27.945806",
        user_id=user_mock.id,
        action="TRANSACTION_CHECK",
        transaction_id="0x09533be63ad3fb86c56fe363562294713578ac110119a71fae3efd03d1d7fe87",
        details="Sample details"
    )
    mock_db.query.return_value.filter_by.return_value.all.return_value = [audit_log_mock]

    # Make the request
    response = test_client.get("/audit-trail", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == str(audit_log_mock.id)


@patch("app.api.endpoints.audit_trail.get_current_user")
def test_unauthorized_access_invalid_jwt(mock_get_current_user, test_client):
    mock_get_current_user.side_effect = Exception("Invalid JWT token")
    
    # Make the request with invalid token
    response = test_client.get("/audit-trail", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_no_jwt_provided(test_client):
    # Make the request without a token
    response = test_client.get("/audit-trail")
    assert response.status_code == 400
    assert response.json() == {"detail": "Not authenticated"}


@patch("app.api.endpoints.audit_trail.get_current_user")
@patch("app.api.endpoints.audit_trail.get_db")
def test_empty_audit_logs(mock_get_db, mock_get_current_user, test_client):
    # Mock the authenticated user
    user_mock = MagicMock()
    user_mock.id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_current_user.return_value = user_mock

    # Mock the database query to return no logs
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_db.query.return_value.filter_by.return_value.all.return_value = []

    # Make the request
    response = test_client.get("/audit-trail", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.json() == []