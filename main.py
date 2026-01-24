"""
E-commerce FastAPI Application

A simple e-commerce platform with modules for:
- User management
- Product management
- Shopping cart
- Order management (with XML export)
"""

from fastapi import FastAPI

from app.routers import (
    auth_router,
    users_router,
    products_router,
    cart_router,
    orders_router,
)

app = FastAPI(
    title="E-commerce API",
    description="A simple e-commerce platform API",
    version="1.0.0",
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to E-commerce API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
