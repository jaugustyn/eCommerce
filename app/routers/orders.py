"""
Orders router - API endpoints for order management.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from app.database.db import db
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService(db)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """Create order from user's cart."""
    order = order_service.create_order_from_cart(order_data.user_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or insufficient stock",
        )
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


@router.get("/", response_model=List[OrderResponse])
async def get_orders(user_id: int = None):
    """Get all orders, optionally filtered by user."""
    if user_id:
        orders = order_service.get_orders_by_user(user_id)
    else:
        orders = order_service.get_all_orders()

    return [
        OrderResponse(
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
        for order in orders
    ]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """Get order by ID."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
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


@router.get("/{order_id}/xml")
async def get_order_xml(order_id: int):
    """Get order details in XML format."""
    xml_content = order_service.get_order_as_xml(order_id)
    if not xml_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return Response(content=xml_content, media_type="application/xml")


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status_value: str):
    """Update order status."""
    try:
        new_status = OrderStatus(status_value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid values: {[s.value for s in OrderStatus]}",
        )

    order = order_service.update_order_status(order_id, new_status)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
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


@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int):
    """Cancel order and restore stock."""
    order = order_service.cancel_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not found or cannot be cancelled",
        )
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
