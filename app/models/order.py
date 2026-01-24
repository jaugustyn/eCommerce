"""
Order model for the e-commerce application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    """Represents an item in an order."""

    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    def get_total(self) -> float:
        """Calculate total for this item."""
        return self.unit_price * self.quantity

    def to_dict(self) -> dict:
        """Convert order item to dictionary."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.get_total(),
        }


@dataclass
class Order:
    """Represents an order in the e-commerce system."""

    id: int
    user_id: int
    items: List[OrderItem]
    total: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert order to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "total": self.total,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
