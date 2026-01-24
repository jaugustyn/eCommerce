"""
In-memory database implementation for the e-commerce application.
"""

from typing import Dict, List, Any, Optional


class Database:
    """
    Simple in-memory database for storing application data.
    Uses dictionaries for each entity type.
    """

    def __init__(self):
        self.users: Dict[int, dict] = {}
        self.products: Dict[int, dict] = {}
        self.carts: Dict[int, dict] = {}  # user_id -> cart
        self.orders: Dict[int, dict] = {}

        # Auto-increment counters
        self._user_id_counter: int = 1
        self._product_id_counter: int = 1
        self._order_id_counter: int = 1

    def get_next_user_id(self) -> int:
        """Generate next user ID."""
        user_id = self._user_id_counter
        self._user_id_counter += 1
        return user_id

    def get_next_product_id(self) -> int:
        """Generate next product ID."""
        product_id = self._product_id_counter
        self._product_id_counter += 1
        return product_id

    def get_next_order_id(self) -> int:
        """Generate next order ID."""
        order_id = self._order_id_counter
        self._order_id_counter += 1
        return order_id

    def reset(self):
        """Reset the database - useful for testing."""
        self.users.clear()
        self.products.clear()
        self.carts.clear()
        self.orders.clear()
        self._user_id_counter = 1
        self._product_id_counter = 1
        self._order_id_counter = 1


# Global database instance
db = Database()
