"""
Cart service - business logic for shopping cart management.
"""

from typing import Optional

from app.database.db import Database
from app.models.cart import Cart, CartItem


class CartService:
    """Service for managing shopping carts."""

    def __init__(self, db: Database):
        self.db = db

    def get_cart(self, user_id: int) -> Cart:
        """Get or create cart for user."""
        if user_id not in self.db.carts:
            self.db.carts[user_id] = Cart(user_id=user_id)
        return self.db.carts[user_id]

    def add_item(self, user_id: int, product_id: int, quantity: int) -> Optional[Cart]:
        """Add item to cart."""
        # Check if product exists
        product = self.db.products.get(product_id)
        if not product:
            return None

        # Check stock availability
        if product.stock < quantity:
            return None

        cart = self.get_cart(user_id)

        # Check if item already in cart
        for item in cart.items:
            if item.product_id == product_id:
                # Check if total quantity exceeds stock
                if product.stock < item.quantity + quantity:
                    return None
                item.quantity += quantity
                return cart

        # Add new item
        cart_item = CartItem(
            product_id=product_id,
            quantity=quantity,
            product_name=product.name,
            unit_price=product.price,
        )
        cart.items.append(cart_item)
        return cart

    def remove_item(self, user_id: int, product_id: int) -> Optional[Cart]:
        """Remove item from cart."""
        cart = self.get_cart(user_id)

        for i, item in enumerate(cart.items):
            if item.product_id == product_id:
                cart.items.pop(i)
                return cart

        return None  # Item not found

    def update_item_quantity(
        self, user_id: int, product_id: int, quantity: int
    ) -> Optional[Cart]:
        """Update item quantity in cart."""
        if quantity <= 0:
            return self.remove_item(user_id, product_id)

        product = self.db.products.get(product_id)
        if not product or product.stock < quantity:
            return None

        cart = self.get_cart(user_id)

        for item in cart.items:
            if item.product_id == product_id:
                item.quantity = quantity
                return cart

        return None  # Item not found

    def clear_cart(self, user_id: int) -> Cart:
        """Clear all items from cart."""
        cart = self.get_cart(user_id)
        cart.items.clear()
        return cart
