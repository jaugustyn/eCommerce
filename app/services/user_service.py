"""
User service - business logic for user management.
"""

import hashlib
from typing import List, Optional

from app.database.db import Database
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for managing users."""

    def __init__(self, db: Database):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        user_id = self.db.get_next_user_id()
        user = User(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=self._hash_password(user_data.password),
        )
        self.db.users[user_id] = user
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.users.get(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users."""
        return list(self.db.users.values())

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user data."""
        user = self.db.users.get(user_id)
        if not user:
            return None

        if user_data.email is not None:
            user.email = user_data.email
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.password is not None:
            user.hashed_password = self._hash_password(user_data.password)
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        if user_id in self.db.users:
            del self.db.users[user_id]
            return True
        return False

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        for user in self.db.users.values():
            if user.email == email:
                return user
        return None
