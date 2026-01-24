"""Reviews router - API endpoints for product reviews."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.db import db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ProductRatingResponse,
)
from app.services.review_service import ReviewService
from app.services.product_service import ProductService

router = APIRouter(prefix="/reviews", tags=["reviews"])
review_service = ReviewService(db)
product_service = ProductService(db)


def _build_review_response(review) -> ReviewResponse:
    """Helper to build ReviewResponse from review model."""
    return ReviewResponse(
        id=review.id,
        product_id=review.product_id,
        user_id=review.user_id,
        rating=review.rating,
        title=review.title,
        comment=review.comment,
        is_verified_purchase=review.is_verified_purchase,
        created_at=review.created_at,
    )


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
):
    """Create a new review for a product."""
    # Check if product exists
    product = product_service.get_product(review_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Check if user has purchased the product (verified purchase)
    is_verified = review_service.check_verified_purchase(
        current_user.id, review_data.product_id
    )

    review = review_service.create_review(
        user_id=current_user.id,
        review_data=review_data,
        is_verified=is_verified,
    )

    if not review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product",
        )

    return _build_review_response(review)


@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: int):
    """Get all reviews for a product."""
    # Check if product exists
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    reviews = review_service.get_product_reviews(product_id)
    return [_build_review_response(review) for review in reviews]


@router.get("/product/{product_id}/rating", response_model=ProductRatingResponse)
async def get_product_rating(product_id: int):
    """Get rating statistics for a product."""
    # Check if product exists
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    stats = review_service.get_product_rating_stats(product_id)
    return ProductRatingResponse(
        product_id=product_id,
        average_rating=stats["average_rating"],
        review_count=stats["review_count"],
        rating_distribution=stats["rating_distribution"],
    )


@router.get("/my", response_model=List[ReviewResponse])
async def get_my_reviews(current_user: User = Depends(get_current_active_user)):
    """Get current user's reviews."""
    reviews = review_service.get_user_reviews(current_user.id)
    return [_build_review_response(review) for review in reviews]


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int):
    """Get review by ID."""
    review = review_service.get_review(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    return _build_review_response(review)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """Update own review."""
    review = review_service.update_review(review_id, current_user.id, review_data)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or access denied",
        )
    return _build_review_response(review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Delete own review."""
    if not review_service.delete_review(review_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or access denied",
        )
    return None
