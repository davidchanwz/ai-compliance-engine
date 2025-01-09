from datetime import timedelta
from app.core.jwt import create_access_token, verify_access_token

def test_create_access_token():
    data = {"sub": "user_id"}
    token = create_access_token(data)
    assert token is not None

def test_verify_access_token():
    data = {"sub": "user_id"}
    token = create_access_token(data)
    decoded_data = verify_access_token(token)
    assert decoded_data["sub"] == "user_id"

def test_expired_token():
    import time
    data = {"sub": "test_user"}
    token = create_access_token(data, expires_delta=timedelta(seconds=1))
    time.sleep(2)  # Wait for the token to expire
    try:
        verify_access_token(token)
    except ValueError as e:
        assert str(e) == "Token has expired"