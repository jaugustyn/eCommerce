"""
Unit tests for product management.
"""

import pytest
from fastapi.testclient import TestClient


class TestProducts:
    """Tests for product endpoints."""

    def test_create_product(self, client: TestClient):
        """Test creating a new product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 29.99,
            "stock": 100,
            "category": "Electronics",
        }
        response = client.post("/products/", json=product_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["price"] == product_data["price"]
        assert data["stock"] == product_data["stock"]
        assert "id" in data

    def test_get_product(self, client: TestClient):
        """Test getting product by ID."""
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 29.99,
            "stock": 100,
            "category": "Electronics",
        }
        create_response = client.post("/products/", json=product_data)
        product_id = create_response.json()["id"]

        response = client.get(f"/products/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == product_data["name"]

    def test_get_product_not_found(self, client: TestClient):
        """Test getting non-existent product."""
        response = client.get("/products/999")

        assert response.status_code == 404

    def test_get_all_products(self, client: TestClient):
        """Test getting all products."""
        for i in range(3):
            client.post("/products/", json={
                "name": f"Product {i}",
                "description": f"Description {i}",
                "price": 10.0 + i,
                "stock": 50,
                "category": "General",
            })

        response = client.get("/products/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_products_by_category(self, client: TestClient):
        """Test filtering products by category."""
        # Create products in different categories
        client.post("/products/", json={
            "name": "Phone",
            "description": "A smartphone",
            "price": 999.99,
            "stock": 10,
            "category": "Electronics",
        })
        client.post("/products/", json={
            "name": "Book",
            "description": "A book",
            "price": 19.99,
            "stock": 100,
            "category": "Books",
        })

        response = client.get("/products/?category=Electronics")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Electronics"

    def test_update_product(self, client: TestClient):
        """Test updating product data."""
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 29.99,
            "stock": 100,
            "category": "Electronics",
        }
        create_response = client.post("/products/", json=product_data)
        product_id = create_response.json()["id"]

        update_data = {"price": 39.99, "stock": 50}
        response = client.put(f"/products/{product_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 39.99
        assert data["stock"] == 50

    def test_delete_product(self, client: TestClient):
        """Test deleting product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product description",
            "price": 29.99,
            "stock": 100,
            "category": "Electronics",
        }
        create_response = client.post("/products/", json=product_data)
        product_id = create_response.json()["id"]

        response = client.delete(f"/products/{product_id}")

        assert response.status_code == 204

        # Verify product is deleted
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 404
