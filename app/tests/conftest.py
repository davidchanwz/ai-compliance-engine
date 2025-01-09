import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_functions import SessionLocal
from app.database.alembic_models import User
from datetime import datetime
from uuid import uuid4
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Define a reusable pytest fixture for TestClient
@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def create_test_user(test_db):
    email = f"test-{uuid4()}@example.com"
    hashed_password = pwd_context.hash("password")
    test_user = User(
        id=str(uuid4()),
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    test_db.add(test_user)
    test_db.commit()
    test_db.refresh(test_user)
    return test_user