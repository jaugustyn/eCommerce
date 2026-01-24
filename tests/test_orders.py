"""
Unit tests for order management.
"""

import pytest
from fastapi.testclient import TestClient


class TestOrders:
    """Tests for order endpoints."""

    def _setup_cart_with_items(self, client: TestClient, user_id: int = 1) -> int:
        """Helper to create a product and add it to cart."""
        # Create product
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 25.00,
            "stock": 100,
            "category": "General",
        }
        product_response = client.post("/products/", json=product_data)
        product_id = product_response.json()["id"]

        # Add to cart
        client.post(f"/cart/{user_id}/items", json={
            "product_id": product_id,
            "quantity": 2,
        })

        return product_id

    def test_create_order(self, client: TestClient):
        """Test creating an order from cart."""
        self._setup_cart_with_items(client, user_id=1)

        response = client.post("/orders/", json={"user_id": 1})

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == 1
        assert len(data["items"]) == 1
        assert data["total"] == 50.00  # 2 * 25.00
        assert data["status"] == "pending"
        assert "id" in data

    def test_create_order_empty_cart(self, client: TestClient):
        """Test creating order with empty cart."""
        response = client.post("/orders/", json={"user_id": 1})

        assert response.status_code == 400

    def test_create_order_clears_cart(self, client: TestClient):
        """Test that creating order clears the cart."""
        self._setup_cart_with_items(client, user_id=1)
        client.post("/orders/", json={"user_id": 1})

        cart_response = client.get("/cart/1")

        assert cart_response.status_code == 200
        assert len(cart_response.json()["items"]) == 0

    def test_create_order_reduces_stock(self, client: TestClient):
        """Test that creating order reduces product stock."""
        product_id = self._setup_cart_with_items(client, user_id=1)
        client.post("/orders/", json={"user_id": 1})

        product_response = client.get(f"/products/{product_id}")

        assert product_response.status_code == 200
        assert product_response.json()["stock"] == 98  # 100 - 2

    def test_get_order(self, client: TestClient):
        """Test getting order by ID."""
        self._setup_cart_with_items(client, user_id=1)
        create_response = client.post("/orders/", json={"user_id": 1})
        order_id = create_response.json()["id"]

        response = client.get(f"/orders/{order_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id

    def test_get_order_not_found(self, client: TestClient):
        """Test getting non-existent order."""
        response = client.get("/orders/999")

        assert response.status_code == 404

    def test_get_order_xml(self, client: TestClient):
        """Test getting order details in XML format."""
        self._setup_cart_with_items(client, user_id=1)
        create_response = client.post("/orders/", json={"user_id": 1})
        order_id = create_response.json()["id"]

        response = client.get(f"/orders/{order_id}/xml")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/xml"
        assert b"<order>" in response.content
        assert b"<id>" in response.content
        assert b"<items>" in response.content

    def test_get_order_xml_not_found(self, client: TestClient):
        """Test getting XML for non-existent order."""
        response = client.get("/orders/999/xml")

        assert response.status_code == 404

    def test_cancel_order(self, client: TestClient):
        """Test cancelling an order."""
        product_id = self._setup_cart_with_items(client, user_id=1)
        create_response = client.post("/orders/", json={"user_id": 1})
        order_id = create_response.json()["id"]

        response = client.post(f"/orders/{order_id}/cancel")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"

        # Verify stock is restored
        product_response = client.get(f"/products/{product_id}")
        assert product_response.json()["stock"] == 100

    def test_get_orders_by_user(self, client: TestClient):
        """Test getting orders filtered by user."""
        # Create orders for different users
        self._setup_cart_with_items(client, user_id=1)
        client.post("/orders/", json={"user_id": 1})

        self._setup_cart_with_items(client, user_id=2)
        client.post("/orders/", json={"user_id": 2})

        response = client.get("/orders/?user_id=1")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_id"] == 1
