"""
Review service - business logic for product reviews.
"""

from typing import List, Optional, Dict

from app.database.db import Database
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:
    """Service for managing product reviews."""

    def __init__(self, db: Database):
        self.db = db

    def create_review(
        self, user_id: int, review_data: ReviewCreate, is_verified: bool = False
    ) -> Optional[Review]:
        """Create a new review."""
        # Check if user already reviewed this product
        existing = self.get_user_review_for_product(user_id, review_data.product_id)
        if existing:
            return None  # User already reviewed this product

        review_id = self.db.get_next_review_id()
        review = Review(
            id=review_id,
            product_id=review_data.product_id,
            user_id=user_id,
            rating=review_data.rating,
            title=review_data.title,
            comment=review_data.comment,
            is_verified_purchase=is_verified,
        )
        self.db.reviews[review_id] = review
        return review

    def get_review(self, review_id: int) -> Optional[Review]:
        """Get review by ID."""
        return self.db.reviews.get(review_id)

    def get_product_reviews(self, product_id: int) -> List[Review]:
        """Get all reviews for a product."""
        return [
            review for review in self.db.reviews.values()
            if review.product_id == product_id
        ]

    def get_user_reviews(self, user_id: int) -> List[Review]:
        """Get all reviews by a user."""
        return [
            review for review in self.db.reviews.values()
            if review.user_id == user_id
        ]

    def get_user_review_for_product(
        self, user_id: int, product_id: int
    ) -> Optional[Review]:
        """Get user's review for a specific product."""
        for review in self.db.reviews.values():
            if review.user_id == user_id and review.product_id == product_id:
                return review
        return None

    def update_review(
        self, review_id: int, user_id: int, review_data: ReviewUpdate
    ) -> Optional[Review]:
        """Update review data (only by owner)."""
        review = self.db.reviews.get(review_id)
        if not review or review.user_id != user_id:
            return None

        if review_data.rating is not None:
            review.rating = review_data.rating
        if review_data.title is not None:
            review.title = review_data.title
        if review_data.comment is not None:
            review.comment = review_data.comment

        return review

    def delete_review(self, review_id: int, user_id: int) -> bool:
        """Delete review by ID (only by owner)."""
        review = self.db.reviews.get(review_id)
        if review and review.user_id == user_id:
            del self.db.reviews[review_id]
            return True
        return False

    def get_product_rating_stats(self, product_id: int) -> Dict:
        """Get rating statistics for a product."""
        reviews = self.get_product_reviews(product_id)

        if not reviews:
            return {
                "average_rating": 0.0,
                "review_count": 0,
                "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            }

        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_rating = 0

        for review in reviews:
            rating_distribution[review.rating] += 1
            total_rating += review.rating

        average_rating = round(total_rating / len(reviews), 2)

        return {
            "average_rating": average_rating,
            "review_count": len(reviews),
            "rating_distribution": rating_distribution,
        }

    def check_verified_purchase(self, user_id: int, product_id: int) -> bool:
        """Check if user has purchased the product (verified purchase)."""
        # Check orders for this user containing this product
        for order in self.db.orders.values():
            if order.user_id == user_id:
                for item in order.items:
                    if item.product_id == product_id:
                        return True
        return False
