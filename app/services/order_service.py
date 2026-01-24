"""
Order service - business logic for order management.
"""

from typing import List, Optional

import dicttoxml

from app.database.db import Database
from app.models.order import Order, OrderItem, OrderStatus


class OrderService:
    """Service for managing orders."""

    def __init__(self, db: Database):
        self.db = db

    def create_order_from_cart(self, user_id: int) -> Optional[Order]:
        """Create order from user's cart."""
        # Get cart
        cart = self.db.carts.get(user_id)
        if not cart or not cart.items:
            return None

        # Validate stock and create order items
        order_items = []
        total = 0.0

        for cart_item in cart.items:
            product = self.db.products.get(cart_item.product_id)
            if not product or product.stock < cart_item.quantity:
                return None  # Insufficient stock

            order_item = OrderItem(
                product_id=cart_item.product_id,
                product_name=product.name,
                quantity=cart_item.quantity,
                unit_price=product.price,
            )
            order_items.append(order_item)
            total += order_item.get_total()

            # Decrease stock
            product.stock -= cart_item.quantity

        # Create order
        order_id = self.db.get_next_order_id()
        order = Order(
            id=order_id,
            user_id=user_id,
            items=order_items,
            total=total,
        )
        self.db.orders[order_id] = order

        # Clear cart
        cart.items.clear()

        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        return self.db.orders.get(order_id)

    def get_orders_by_user(self, user_id: int) -> List[Order]:
        """Get all orders for a user."""
        return [
            order for order in self.db.orders.values() if order.user_id == user_id
        ]

    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self.db.orders.values())

    def update_order_status(
        self, order_id: int, status: OrderStatus
    ) -> Optional[Order]:
        """Update order status."""
        order = self.db.orders.get(order_id)
        if not order:
            return None

        order.status = status
        return order

    def cancel_order(self, order_id: int) -> Optional[Order]:
        """Cancel order and restore stock."""
        order = self.db.orders.get(order_id)
        if not order:
            return None

        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            return None  # Cannot cancel shipped/delivered orders

        # Restore stock
        for item in order.items:
            product = self.db.products.get(item.product_id)
            if product:
                product.stock += item.quantity

        order.status = OrderStatus.CANCELLED
        return order

    def get_order_as_xml(self, order_id: int) -> Optional[str]:
        """Get order details in XML format."""
        order = self.db.orders.get(order_id)
        if not order:
            return None

        order_dict = order.to_dict()
        xml_bytes = dicttoxml.dicttoxml(
            order_dict,
            custom_root="order",
            attr_type=False
        )
        return xml_bytes.decode("utf-8")
