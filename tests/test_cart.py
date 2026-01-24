"""
Unit tests for shopping cart management.
"""

import pytest
from fastapi.testclient import TestClient


class TestCart:
    """Tests for cart endpoints."""

    def _create_product(self, client: TestClient) -> int:
        """Helper to create a product and return its ID."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 25.00,
            "stock": 100,
            "category": "General",
        }
        response = client.post("/products/", json=product_data)
        return response.json()["id"]

    def test_get_empty_cart(self, client: TestClient):
        """Test getting an empty cart."""
        response = client.get("/cart/1")

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert data["items"] == []
        assert data["total"] == 0.0

    def test_add_item_to_cart(self, client: TestClient):
        """Test adding item to cart."""
        product_id = self._create_product(client)

        response = client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 2,
        })

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == product_id
        assert data["items"][0]["quantity"] == 2
        assert data["total"] == 50.00  # 2 * 25.00

    def test_add_item_nonexistent_product(self, client: TestClient):
        """Test adding non-existent product to cart."""
        response = client.post("/cart/1/items", json={
            "product_id": 999,
            "quantity": 1,
        })

        assert response.status_code == 400

    def test_add_item_insufficient_stock(self, client: TestClient):
        """Test adding item with insufficient stock."""
        product_id = self._create_product(client)

        response = client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 101,  # Stock is 100
        })

        assert response.status_code == 400

    def test_add_same_item_increases_quantity(self, client: TestClient):
        """Test adding same item increases quantity."""
        product_id = self._create_product(client)

        client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 2,
        })
        response = client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 3,
        })

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 5
        assert data["total"] == 125.00  # 5 * 25.00

    def test_remove_item_from_cart(self, client: TestClient):
        """Test removing item from cart."""
        product_id = self._create_product(client)
        client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 2,
        })

        response = client.delete(f"/cart/1/items/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
        assert data["total"] == 0.0

    def test_clear_cart(self, client: TestClient):
        """Test clearing all items from cart."""
        product_id = self._create_product(client)
        client.post("/cart/1/items", json={
            "product_id": product_id,
            "quantity": 5,
        })

        response = client.delete("/cart/1")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
        assert data["total"] == 0.0
