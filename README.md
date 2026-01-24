# E-commerce API - FastAPI

Aplikacja e-commerce zbudowana z FastAPI z autoryzacją JWT i wsparciem Dockera.

## Funkcjonalności

- **Autoryzacja JWT/OAuth2** - Bezpieczna autentykacja z tokenami JWT
- **Zarządzanie użytkownikami** - Rejestracja, logowanie, profile
- **Produkty** - CRUD z filtrowaniem po kategoriach
- **Kategorie** - Kategorie produktów
- **Koszyk** - Zarządzanie koszykiem zakupowym
- **Zamówienia** - Składanie zamówień z eksportem do XML
- **Recenzje** - Oceny i opinie o produktach

## Architektura

Projekt wykorzystuje architekturę warstwową:

```
app/
├── routers/      # Warstwa API - endpointy REST
├── services/     # Warstwa logiki biznesowej  
├── models/       # Modele danych (dataclasses)
├── schemas/      # Schematy Pydantic (walidacja)
├── database/     # Warstwa danych (in-memory)
└── core/         # Konfiguracja, security
```

**Moduły:**
- `users` - zarządzanie użytkownikami
- `products` - zarządzanie produktami
- `cart` - obsługa koszyka zakupowego
- `orders` - zarządzanie zamówieniami (z XML export)
- `categories` - kategorie produktów
- `reviews` - recenzje produktów

## Instalacja

```bash
pipenv install --dev
pipenv run uvicorn main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## Dostęp

- **API**: http://localhost:8000
- **Dokumentacja Swagger**: http://localhost:8000/docs

## Testy

```bash
pipenv run pytest tests/ -v
```

## Technologie

- FastAPI, Pydantic
- python-jose (JWT), passlib + bcrypt
- dicttoxml (eksport XML)
- pytest, Docker
