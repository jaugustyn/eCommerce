"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: int


class LoginRequest(BaseModel):
    """Schema for login request (used with OAuth2PasswordRequestForm)."""

    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
