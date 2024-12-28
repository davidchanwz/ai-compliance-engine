import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Define a reusable pytest fixture for TestClient
@pytest.fixture
def test_client():
    return TestClient(app)