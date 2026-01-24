"""Review model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Review:
    id: int
    product_id: int
    user_id: int
    rating: int  # 1-5
    title: str
    comment: str
    is_verified_purchase: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "is_verified_purchase": self.is_verified_purchase,
            "created_at": self.created_at.isoformat(),
        }
