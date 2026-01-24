"""
Pydantic schemas for Cart.
"""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):
    """Schema for adding item to cart."""

    product_id: int = Field(..., description="Product ID to add to cart")
    quantity: int = Field(..., gt=0, description="Quantity to add")


class CartItemResponse(BaseModel):
    """Schema for cart item response."""

    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    """Schema for cart response."""

    user_id: int
    items: List[CartItemResponse]
    total: float

    model_config = ConfigDict(from_attributes=True)
