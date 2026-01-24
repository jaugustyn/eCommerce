"""
Product model for the e-commerce application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Product:
    """Represents a product in the e-commerce system."""

    id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert product to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
        }
