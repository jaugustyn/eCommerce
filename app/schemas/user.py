"""
Pydantic schemas for User.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base schema for user data."""

    email: str = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, description="User full name")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=6, description="User password")


class UserUpdate(BaseModel):
    """Schema for updating user data."""

    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, min_length=1, description="User full name")
    password: Optional[str] = Field(None, min_length=6, description="User password")
    is_active: Optional[bool] = Field(None, description="User active status")


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
