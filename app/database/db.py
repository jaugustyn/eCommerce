"""
In-memory database implementation for the e-commerce application.
"""

from typing import Dict


class Database:
    """
    Simple in-memory database using dictionaries for each entity type.
    """

    def __init__(self):
        self.users: Dict[int, dict] = {}
        self.products: Dict[int, dict] = {}
        self.carts: Dict[int, dict] = {}
        self.orders: Dict[int, dict] = {}
        self.categories: Dict[int, dict] = {}
        self.reviews: Dict[int, dict] = {}

        self._user_id_counter: int = 1
        self._product_id_counter: int = 1
        self._order_id_counter: int = 1
        self._category_id_counter: int = 1
        self._review_id_counter: int = 1

    def get_next_user_id(self) -> int:
        user_id = self._user_id_counter
        self._user_id_counter += 1
        return user_id

    def get_next_product_id(self) -> int:
        product_id = self._product_id_counter
        self._product_id_counter += 1
        return product_id

    def get_next_order_id(self) -> int:
        order_id = self._order_id_counter
        self._order_id_counter += 1
        return order_id

    def get_next_category_id(self) -> int:
        category_id = self._category_id_counter
        self._category_id_counter += 1
        return category_id

    def get_next_review_id(self) -> int:
        review_id = self._review_id_counter
        self._review_id_counter += 1
        return review_id

    def reset(self):
        """Reset database - useful for testing."""
        self.users.clear()
        self.products.clear()
        self.carts.clear()
        self.orders.clear()
        self.categories.clear()
        self.reviews.clear()
        self._user_id_counter = 1
        self._product_id_counter = 1
        self._order_id_counter = 1
        self._category_id_counter = 1
        self._review_id_counter = 1


db = Database()
