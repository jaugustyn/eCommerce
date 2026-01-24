"""Pydantic schemas for Review."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    """Base schema for review data."""

    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 stars)")
    title: str = Field(..., min_length=1, max_length=200, description="Review title")
    comment: str = Field(..., min_length=10, description="Review comment")


class ReviewCreate(ReviewBase):
    """Schema for creating a new review."""

    product_id: int = Field(..., description="Product ID to review")


class ReviewUpdate(BaseModel):
    """Schema for updating review data."""

    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    comment: Optional[str] = Field(None, min_length=10)


class ReviewResponse(ReviewBase):
    """Schema for review response."""

    id: int
    product_id: int
    user_id: int
    is_verified_purchase: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewWithUserResponse(ReviewResponse):
    """Schema for review response with user info."""

    user_name: str


class ProductRatingResponse(BaseModel):
    """Schema for product rating summary."""

    product_id: int
    average_rating: float
    review_count: int
    rating_distribution: dict  # {1: count, 2: count, ...}
