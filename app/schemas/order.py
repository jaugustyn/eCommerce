"""
Pydantic schemas for Order.
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class OrderItemResponse(BaseModel):
    """Schema for order item response."""

    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """Schema for creating an order from cart."""

    user_id: int = Field(..., description="User ID placing the order")


class OrderResponse(BaseModel):
    """Schema for order response."""

    id: int
    user_id: int
    items: List[OrderItemResponse]
    total: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
