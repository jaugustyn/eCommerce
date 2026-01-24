"""
API routers for the e-commerce application.
"""

from .auth import router as auth_router
from .users import router as users_router
from .products import router as products_router
from .cart import router as cart_router
from .orders import router as orders_router

__all__ = [
    "auth_router",
    "users_router",
    "products_router",
    "cart_router",
    "orders_router",
]
