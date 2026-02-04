# E-commerce API - FastAPI

E-commerce application built with FastAPI featuring JWT authentication.

## Features

- **JWT/OAuth2 Authentication** - Secure authentication with JWT tokens
- **User Management** - Registration, login, profiles
- **Products** - CRUD operations with category filtering
- **Categories** - Product categories
- **Shopping Cart** - Cart management
- **Orders** - Order placement with XML export
- **Reviews** - Product ratings and reviews

## Architecture

The project uses a layered architecture:

```
app/
├── routers/      # API layer - REST endpoints
├── services/     # Business logic layer
├── models/       # Data models (dataclasses)
├── schemas/      # Pydantic schemas (validation)
├── database/     # Data layer (in-memory)
└── core/         # Configuration, security
```

**Modules:**
- `users` - user management
- `products` - product management
- `cart` - shopping cart handling
- `orders` - order management (with XML export)
- `categories` - product categories
- `reviews` - product reviews

## Installation

```bash
pipenv install --dev
pipenv run uvicorn main:app --reload
```

## Access

- **API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs

## Tests

```bash
pipenv run pytest tests/ -v
```

## Technologies

- FastAPI, Pydantic
- python-jose (JWT), passlib + bcrypt
- dicttoxml (XML export)
- pytest, Docker
