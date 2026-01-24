"""
Cart model for the e-commerce application.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CartItem:
    """Represents an item in the shopping cart."""

    product_id: int
    quantity: int
    product_name: str = ""
    unit_price: float = 0.0

    def to_dict(self) -> dict:
        """Convert cart item to dictionary."""
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product_name": self.product_name,
            "unit_price": self.unit_price,
            "total_price": self.unit_price * self.quantity,
        }


@dataclass
class Cart:
    """Represents a user's shopping cart."""

    user_id: int
    items: List[CartItem] = field(default_factory=list)

    def get_total(self) -> float:
        """Calculate total cart value."""
        return sum(item.unit_price * item.quantity for item in self.items)

    def to_dict(self) -> dict:
        """Convert cart to dictionary."""
        return {
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "total": self.get_total(),
        }
