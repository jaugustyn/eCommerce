"""
Orders router - API endpoints for order management.
Requires authentication for most operations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.database.db import db
from app.dependencies import get_current_active_user
from app.models.order import OrderStatus
from app.models.user import User
from app.schemas.order import OrderResponse, OrderItemResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService(db)


def _build_order_response(order) -> OrderResponse:
    """Helper to build OrderResponse from order model."""
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        items=[
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.get_total(),
            )
            for item in order.items
        ],
        total=order.total,
        status=order.status.value,
        created_at=order.created_at,
    )


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(current_user: User = Depends(get_current_active_user)):
    """Create order from current user's cart."""
    order = order_service.create_order_from_cart(current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or insufficient stock",
        )
    return _build_order_response(order)


@router.get("/", response_model=List[OrderResponse])
async def get_my_orders(current_user: User = Depends(get_current_active_user)):
    """Get current user's orders."""
    orders = order_service.get_orders_by_user(current_user.id)
    return [_build_order_response(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Get order by ID (only own orders)."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    # Check if order belongs to current user
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return _build_order_response(order)


@router.get("/{order_id}/xml")
async def get_order_xml(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Get order details in XML format (only own orders)."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    # Check if order belongs to current user
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    xml_content = order_service.get_order_as_xml(order_id)
    return Response(content=xml_content, media_type="application/xml")


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_value: str,
    current_user: User = Depends(get_current_active_user),
):
    """Update order status (only own orders, limited statuses)."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    try:
        new_status = OrderStatus(status_value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid values: {[s.value for s in OrderStatus]}",
        )

    updated_order = order_service.update_order_status(order_id, new_status)
    return _build_order_response(updated_order)


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """Cancel order and restore stock (only own orders)."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    cancelled_order = order_service.cancel_order(order_id)
    if not cancelled_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled (already shipped/delivered)",
        )
    return _build_order_response(cancelled_order)
