"""
Pydantic schemas for Product.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Base schema for product data."""

    name: str = Field(..., min_length=1, description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(..., ge=0, description="Available stock quantity")
    category: str = Field(..., min_length=1, description="Product category")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating product data."""

    name: Optional[str] = Field(None, min_length=1, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, gt=0, description="Product price")
    stock: Optional[int] = Field(None, ge=0, description="Available stock quantity")
    category: Optional[str] = Field(None, min_length=1, description="Product category")


class ProductResponse(ProductBase):
    """Schema for product response."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
