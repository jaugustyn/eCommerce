"""
Categories router - API endpoints for category management.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.database.db import db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])
category_service = CategoryService(db)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    """Create a new category."""
    # Check if name already exists
    existing = category_service.get_category_by_name(category_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    # Validate parent_id if provided
    if category_data.parent_id:
        parent = category_service.get_category(category_data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )

    category = category_service.create_category(category_data)
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        parent_id=category.parent_id,
        created_at=category.created_at,
    )


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(root_only: bool = False):
    """Get all categories, optionally only root categories."""
    if root_only:
        categories = category_service.get_root_categories()
    else:
        categories = category_service.get_all_categories()

    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            parent_id=cat.parent_id,
            created_at=cat.created_at,
        )
        for cat in categories
    ]


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int):
    """Get category by ID."""
    category = category_service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        parent_id=category.parent_id,
        created_at=category.created_at,
    )


@router.get("/{category_id}/subcategories", response_model=List[CategoryResponse])
async def get_subcategories(category_id: int):
    """Get subcategories of a category."""
    # Verify parent exists
    parent = category_service.get_category(category_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    subcategories = category_service.get_subcategories(category_id)
    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            parent_id=cat.parent_id,
            created_at=cat.created_at,
        )
        for cat in subcategories
    ]


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category_data: CategoryUpdate):
    """Update category data."""
    category = category_service.update_category(category_id, category_data)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        parent_id=category.parent_id,
        created_at=category.created_at,
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    """Delete category by ID."""
    if not category_service.delete_category(category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return None
