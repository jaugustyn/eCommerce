# E-commerce API - FastAPI

Aplikacja e-commerce zbudowana z użyciem FastAPI, implementująca podstawowe funkcjonalności platformy sklepowej.

## Struktura projektu

```
eCommerce/
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py              # In-memory database
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # Model użytkownika
│   │   ├── product.py         # Model produktu
│   │   ├── cart.py            # Model koszyka
│   │   └── order.py           # Model zamówienia
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # Schematy Pydantic dla użytkowników
│   │   ├── product.py         # Schematy Pydantic dla produktów
│   │   ├── cart.py            # Schematy Pydantic dla koszyka
│   │   └── order.py           # Schematy Pydantic dla zamówień
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py           # Endpointy API dla użytkowników
│   │   ├── products.py        # Endpointy API dla produktów
│   │   ├── cart.py            # Endpointy API dla koszyka
│   │   └── orders.py          # Endpointy API dla zamówień
│   └── services/
│       ├── __init__.py
│       ├── user_service.py    # Logika biznesowa użytkowników
│       ├── product_service.py # Logika biznesowa produktów
│       ├── cart_service.py    # Logika biznesowa koszyka
│       └── order_service.py   # Logika biznesowa zamówień + XML
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Konfiguracja pytest i fixtures
│   ├── test_users.py          # Testy użytkowników
│   ├── test_products.py       # Testy produktów
│   ├── test_cart.py           # Testy koszyka
│   └── test_orders.py         # Testy zamówień
├── main.py                    # Główny plik aplikacji
├── Pipfile                    # Zależności projektu
├── Pipfile.lock
└── README.md
```

## Moduły

### 1. Użytkownicy (`/users`)
- `POST /users/` - Tworzenie nowego użytkownika
- `GET /users/` - Lista wszystkich użytkowników
- `GET /users/{id}` - Szczegóły użytkownika
- `PUT /users/{id}` - Aktualizacja użytkownika
- `DELETE /users/{id}` - Usunięcie użytkownika

### 2. Produkty (`/products`)
- `POST /products/` - Dodawanie nowego produktu
- `GET /products/` - Lista produktów (opcjonalnie filtrowanie po kategorii)
- `GET /products/{id}` - Szczegóły produktu
- `PUT /products/{id}` - Aktualizacja produktu
- `DELETE /products/{id}` - Usunięcie produktu

### 3. Koszyk (`/cart`)
- `GET /cart/{user_id}` - Pobranie koszyka użytkownika
- `POST /cart/{user_id}/items` - Dodanie produktu do koszyka
- `PUT /cart/{user_id}/items/{product_id}` - Aktualizacja ilości produktu
- `DELETE /cart/{user_id}/items/{product_id}` - Usunięcie produktu z koszyka
- `DELETE /cart/{user_id}` - Wyczyszczenie koszyka

### 4. Zamówienia (`/orders`)
- `POST /orders/` - Utworzenie zamówienia z koszyka
- `GET /orders/` - Lista zamówień (opcjonalnie filtrowanie po użytkowniku)
- `GET /orders/{id}` - Szczegóły zamówienia
- `GET /orders/{id}/xml` - **Szczegóły zamówienia w formacie XML**
- `PUT /orders/{id}/status` - Aktualizacja statusu zamówienia
- `POST /orders/{id}/cancel` - Anulowanie zamówienia

## Instalacja

```bash
# Klonowanie repozytorium
cd eCommerce

# Instalacja zależności
pipenv install --dev

# Aktywacja środowiska wirtualnego
pipenv shell
```

## Uruchomienie

```bash
# Uruchomienie serwera deweloperskiego
uvicorn main:app --reload

# Lub przez pipenv
pipenv run uvicorn main:app --reload
```

Aplikacja będzie dostępna pod adresem: http://localhost:8000

Dokumentacja API (Swagger UI): http://localhost:8000/docs

## Testy

```bash
# Uruchomienie wszystkich testów
pipenv run pytest tests/ -v

# Uruchomienie testów z pokryciem kodu
pipenv run pytest tests/ -v --cov=app
```

## Technologie

- **FastAPI** - Framework webowy
- **Pydantic** - Walidacja danych
- **dicttoxml** - Konwersja do XML
- **pytest** - Framework do testów
- **httpx** - Klient HTTP dla testów

## Standardy kodu

Projekt jest zgodny ze standardem **PEP-8**:
- Formatowanie kodu zgodne z PEP-8
- Docstringi dla klas i funkcji
- Type hints dla parametrów i wartości zwracanych
- Maksymalna długość linii: 88 znaków

## Przykłady użycia API

### Tworzenie użytkownika
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "jan@example.com", "full_name": "Jan Kowalski", "password": "haslo123"}'
```

### Dodawanie produktu
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Laptop gamingowy", "price": 4999.99, "stock": 10, "category": "Elektronika"}'
```

### Dodawanie do koszyka
```bash
curl -X POST "http://localhost:8000/cart/1/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Tworzenie zamówienia
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

### Pobieranie zamówienia w XML
```bash
curl "http://localhost:8000/orders/1/xml"
```

## Autor

Projekt przygotowany jako zadanie projektowe z użyciem FastAPI.
