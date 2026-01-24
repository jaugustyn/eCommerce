"""
Cart router - API endpoints for shopping cart management.
"""

from fastapi import APIRouter, HTTPException, status

from app.database.db import db
from app.schemas.cart import CartItemCreate, CartResponse, CartItemResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])
cart_service = CartService(db)


@router.get("/{user_id}", response_model=CartResponse)
async def get_cart(user_id: int):
    """Get cart for a user."""
    cart = cart_service.get_cart(user_id)
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


@router.post("/{user_id}/items", response_model=CartResponse)
async def add_item_to_cart(user_id: int, item: CartItemCreate):
    """Add item to cart."""
    cart = cart_service.add_item(user_id, item.product_id, item.quantity)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found or insufficient stock",
        )
    return CartResponse(
        user_id=cart.user_id,
        items=[
            CartItemResponse(
                product_id=cart_item.product_id,
                product_name=cart_item.product_name,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.unit_price * cart_item.quantity,
            )
            for cart_item in cart.items
        ],
        total=cart.get_total(),
    )


@router.delete("/{user_id}/items/{product_id}", response_model=CartResponse)
async def remove_item_from_cart(user_id: int, product_id: int):
    """Remove item from cart."""
    cart = cart_service.remove_item(user_id, product_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart",
        )
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


@router.put("/{user_id}/items/{product_id}", response_model=CartResponse)
async def update_cart_item(user_id: int, product_id: int, item: CartItemCreate):
    """Update item quantity in cart."""
    cart = cart_service.update_item_quantity(user_id, product_id, item.quantity)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item not found or insufficient stock",
        )
    return CartResponse(
        user_id=cart.user_id,
        items=[
            CartItemResponse(
                product_id=cart_item.product_id,
                product_name=cart_item.product_name,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.unit_price * cart_item.quantity,
            )
            for cart_item in cart.items
        ],
        total=cart.get_total(),
    )


@router.delete("/{user_id}", response_model=CartResponse)
async def clear_cart(user_id: int):
    """Clear all items from cart."""
    cart = cart_service.clear_cart(user_id)
    return CartResponse(
        user_id=cart.user_id,
        items=[],
        total=0.0,
    )
