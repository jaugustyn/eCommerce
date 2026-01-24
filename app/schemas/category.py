"""
Pydantic schemas for Category.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """Base schema for category data."""

    name: str = Field(..., min_length=1, description="Category name")
    description: str = Field(..., description="Category description")


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""

    parent_id: Optional[int] = Field(None, description="Parent category ID")


class CategoryUpdate(BaseModel):
    """Schema for updating category data."""

    name: Optional[str] = Field(None, min_length=1, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    parent_id: Optional[int] = Field(None, description="Parent category ID")


class CategoryResponse(CategoryBase):
    """Schema for category response."""

    id: int
    parent_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
