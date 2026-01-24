"""
Pytest configuration and fixtures for e-commerce tests.
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from app.database.db import db
from app.core.security import get_password_hash
from app.models.user import User


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test."""
    db.reset()
    yield
    db.reset()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_client(client):
    """Create authenticated test client with test user."""
    # Create test user directly in database
    user_id = db.get_next_user_id()
    test_user = User(
        id=user_id,
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
    )
    db.users[user_id] = test_user

    # Login and get token
    response = client.post(
        "/auth/login",
        data={"username": "testuser@example.com", "password": "testpassword123"},
    )
    token = response.json()["access_token"]

    # Add auth header to client
    client.headers["Authorization"] = f"Bearer {token}"
    client.test_user_id = user_id
    return client

