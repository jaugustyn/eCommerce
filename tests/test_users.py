"""
Unit tests for user management.
"""

from fastapi.testclient import TestClient


class TestUsers:
    """Tests for user endpoints."""

    def test_create_user(self, client: TestClient):
        """Test creating a new user."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }
        response = client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert data["is_active"] is True

    def test_create_user_duplicate_email(self, client: TestClient):
        """Test creating user with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }
        client.post("/users/", json=user_data)
        response = client.post("/users/", json=user_data)

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_get_user(self, client: TestClient):
        """Test getting user by ID."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]

    def test_get_user_not_found(self, client: TestClient):
        """Test getting non-existent user."""
        response = client.get("/users/999")

        assert response.status_code == 404

    def test_get_all_users(self, client: TestClient):
        """Test getting all users."""
        # Create multiple users
        for i in range(3):
            client.post("/users/", json={
                "email": f"user{i}@example.com",
                "full_name": f"User {i}",
                "password": "password123",
            })

        response = client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_update_user(self, client: TestClient):
        """Test updating user data."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        update_data = {"full_name": "Updated Name"}
        response = client.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"

    def test_delete_user(self, client: TestClient):
        """Test deleting user."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepassword123",
        }
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 204

        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
