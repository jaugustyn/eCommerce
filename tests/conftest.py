"""
Pytest configuration and fixtures for e-commerce tests.
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from app.database.db import db


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test."""
    db.reset()
    yield
    db.reset()
