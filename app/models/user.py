"""
User model for the e-commerce application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a user in the e-commerce system."""

    id: int
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
