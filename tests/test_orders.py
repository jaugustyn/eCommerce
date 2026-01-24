"""
Unit tests for order management.
"""

import pytest
from fastapi.testclient import TestClient


class TestOrders:
    """Tests for order endpoints."""

    def _setup_cart_with_items(self, auth_client: TestClient) -> int:
        """Helper to create a product and add it to cart."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 25.00,
            "stock": 100,
            "category": "General",
        }
        product_response = auth_client.post("/products/", json=product_data)
        product_id = product_response.json()["id"]

        auth_client.post("/cart/items", json={
            "product_id": product_id,
            "quantity": 2,
        })

        return product_id

    def test_create_order(self, auth_client: TestClient):
        """Test creating an order from cart."""
        self._setup_cart_with_items(auth_client)

        response = auth_client.post("/orders/")

        assert response.status_code == 201
        data = response.json()
        assert len(data["items"]) == 1
        assert data["total"] == 50.00  # 2 * 25.00
        assert data["status"] == "pending"
        assert "id" in data

    def test_create_order_empty_cart(self, auth_client: TestClient):
        """Test creating order with empty cart."""
        response = auth_client.post("/orders/")

        assert response.status_code == 400

    def test_create_order_clears_cart(self, auth_client: TestClient):
        """Test that creating order clears the cart."""
        self._setup_cart_with_items(auth_client)
        auth_client.post("/orders/")

        cart_response = auth_client.get("/cart/")

        assert cart_response.status_code == 200
        assert len(cart_response.json()["items"]) == 0

    def test_create_order_reduces_stock(self, auth_client: TestClient):
        """Test that creating order reduces product stock."""
        product_id = self._setup_cart_with_items(auth_client)
        auth_client.post("/orders/")

        product_response = auth_client.get(f"/products/{product_id}")

        assert product_response.status_code == 200
        assert product_response.json()["stock"] == 98  # 100 - 2

    def test_get_order(self, auth_client: TestClient):
        """Test getting order by ID."""
        self._setup_cart_with_items(auth_client)
        create_response = auth_client.post("/orders/")
        order_id = create_response.json()["id"]

        response = auth_client.get(f"/orders/{order_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id

    def test_get_order_not_found(self, auth_client: TestClient):
        """Test getting non-existent order."""
        response = auth_client.get("/orders/999")

        assert response.status_code == 404

    def test_get_order_xml(self, auth_client: TestClient):
        """Test getting order details in XML format."""
        self._setup_cart_with_items(auth_client)
        create_response = auth_client.post("/orders/")
        order_id = create_response.json()["id"]

        response = auth_client.get(f"/orders/{order_id}/xml")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/xml"
        assert b"<order>" in response.content
        assert b"<id>" in response.content
        assert b"<items>" in response.content

    def test_get_order_xml_not_found(self, auth_client: TestClient):
        """Test getting XML for non-existent order."""
        response = auth_client.get("/orders/999/xml")

        assert response.status_code == 404

    def test_cancel_order(self, auth_client: TestClient):
        """Test cancelling an order."""
        product_id = self._setup_cart_with_items(auth_client)
        create_response = auth_client.post("/orders/")
        order_id = create_response.json()["id"]

        response = auth_client.post(f"/orders/{order_id}/cancel")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"

        # Verify stock is restored
        product_response = auth_client.get(f"/products/{product_id}")
        assert product_response.json()["stock"] == 100

    def test_get_my_orders(self, auth_client: TestClient):
        """Test getting current user's orders."""
        self._setup_cart_with_items(auth_client)
        auth_client.post("/orders/")

        response = auth_client.get("/orders/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
