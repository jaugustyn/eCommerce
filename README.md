# E-commerce API - FastAPI

Kompleksowa aplikacja e-commerce zbudowana z FastAPI z autoryzacją JWT i wsparciem Dockera.

## Funkcjonalności

- **Autoryzacja JWT/OAuth2** - Bezpieczna autentykacja z tokenami JWT
- **Zarządzanie użytkownikami** - Rejestracja, logowanie, profile
- **Produkty** - Pełny CRUD z filtrowaniem po kategoriach
- **Kategorie** - Hierarchiczne kategorie produktów
- **Koszyk** - Zarządzanie koszykiem zakupowym
- **Zamówienia** - Składanie zamówień z eksportem do XML
- **Recenzje** - Oceny i opinie o produktach



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
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testy

```bash
pipenv run pytest tests/ -v
```

## Technologie

- FastAPI, Pydantic
- python-jose (JWT), passlib + bcrypt
- dicttoxml (XML export)
- pytest, Docker
