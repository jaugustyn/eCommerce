"""
Products router - API endpoints for product management.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.database.db import db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])
product_service = ProductService(db)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate):
    """Create a new product."""
    product = product_service.create_product(product_data)
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        created_at=product.created_at,
    )


@router.get("/", response_model=List[ProductResponse])
async def get_products(category: Optional[str] = Query(None, description="Filter by category")):
    """Get all products, optionally filtered by category."""
    if category:
        products = product_service.get_products_by_category(category)
    else:
        products = product_service.get_all_products()

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category,
            created_at=product.created_at,
        )
        for product in products
    ]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Get product by ID."""
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        created_at=product.created_at,
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: ProductUpdate):
    """Update product data."""
    product = product_service.update_product(product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        created_at=product.created_at,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    """Delete product by ID."""
    if not product_service.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return None
