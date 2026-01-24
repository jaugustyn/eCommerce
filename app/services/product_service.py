"""
Product service - business logic for product management.
"""

from typing import List, Optional

from app.database.db import Database
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Service for managing products."""

    def __init__(self, db: Database):
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        product_id = self.db.get_next_product_id()
        product = Product(
            id=product_id,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            category=product_data.category,
        )
        self.db.products[product_id] = product
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return self.db.products.get(product_id)

    def get_all_products(self) -> List[Product]:
        """Get all products."""
        return list(self.db.products.values())

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category."""
        return [
            product
            for product in self.db.products.values()
            if product.category.lower() == category.lower()
        ]

    def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> Optional[Product]:
        """Update product data."""
        product = self.db.products.get(product_id)
        if not product:
            return None

        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.stock is not None:
            product.stock = product_data.stock
        if product_data.category is not None:
            product.category = product_data.category

        return product

    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID."""
        if product_id in self.db.products:
            del self.db.products[product_id]
            return True
        return False

    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock (negative for decrease)."""
        product = self.db.products.get(product_id)
        if not product:
            return False

        new_stock = product.stock + quantity_change
        if new_stock < 0:
            return False

        product.stock = new_stock
        return True
