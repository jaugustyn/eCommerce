"""
Category service - business logic for category management.
"""

from typing import List, Optional

from app.database.db import Database
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service for managing categories."""

    def __init__(self, db: Database):
        self.db = db

    def create_category(self, category_data: CategoryCreate) -> Category:
        """Create a new category."""
        category_id = self.db.get_next_category_id()
        category = Category(
            id=category_id,
            name=category_data.name,
            description=category_data.description,
            parent_id=category_data.parent_id,
        )
        self.db.categories[category_id] = category
        return category

    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return self.db.categories.get(category_id)

    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        return list(self.db.categories.values())

    def get_root_categories(self) -> List[Category]:
        """Get all root categories (no parent)."""
        return [
            cat for cat in self.db.categories.values()
            if cat.parent_id is None
        ]

    def get_subcategories(self, parent_id: int) -> List[Category]:
        """Get all subcategories of a category."""
        return [
            cat for cat in self.db.categories.values()
            if cat.parent_id == parent_id
        ]

    def update_category(
        self, category_id: int, category_data: CategoryUpdate
    ) -> Optional[Category]:
        """Update category data."""
        category = self.db.categories.get(category_id)
        if not category:
            return None

        if category_data.name is not None:
            category.name = category_data.name
        if category_data.description is not None:
            category.description = category_data.description
        if category_data.parent_id is not None:
            # Prevent circular reference
            if category_data.parent_id != category_id:
                category.parent_id = category_data.parent_id

        return category

    def delete_category(self, category_id: int) -> bool:
        """Delete category by ID."""
        if category_id in self.db.categories:
            # Update products with this category
            # (in real app would need more sophisticated handling)
            del self.db.categories[category_id]
            return True
        return False

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Get category by name."""
        for category in self.db.categories.values():
            if category.name.lower() == name.lower():
                return category
        return None
