"""
Cart router - API endpoints for shopping cart management.
Requires authentication - users can only access their own cart.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.db import db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartResponse, CartItemResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])
cart_service = CartService(db)


def _build_cart_response(cart) -> CartResponse:
    """Helper to build CartResponse from cart model."""
    return CartResponse(
        user_id=cart.user_id,
        items=[
            CartItemResponse(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.unit_price * item.quantity,
            )
            for item in cart.items
        ],
        total=cart.get_total(),
    )


@router.get("/", response_model=CartResponse)
async def get_my_cart(current_user: User = Depends(get_current_active_user)):
    """Get current user's cart."""
    cart = cart_service.get_cart(current_user.id)
    return _build_cart_response(cart)


@router.post("/items", response_model=CartResponse)
async def add_item_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
):
    """Add item to current user's cart."""
    cart = cart_service.add_item(current_user.id, item.product_id, item.quantity)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found or insufficient stock",
        )
    return _build_cart_response(cart)


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_item_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Remove item from current user's cart."""
    cart = cart_service.remove_item(current_user.id, product_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart",
        )
    return _build_cart_response(cart)


@router.put("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: int,
    item: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
):
    """Update item quantity in current user's cart."""
    cart = cart_service.update_item_quantity(
        current_user.id, product_id, item.quantity
    )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item not found or insufficient stock",
        )
    return _build_cart_response(cart)


@router.delete("/", response_model=CartResponse)
async def clear_cart(current_user: User = Depends(get_current_active_user)):
    """Clear all items from current user's cart."""
    cart = cart_service.clear_cart(current_user.id)
    return CartResponse(
        user_id=cart.user_id,
        items=[],
        total=0.0,
    )
