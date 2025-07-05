# Habit Tracker

Aplikacja webowa do zarządzania nawykami, zbudowana w ramach zajęć „Automatyzacja budowy oprogramowania”.

## Funkcjonalności

- Dodawanie, edytowanie i usuwanie nawyków
- Prosty frontend w HTML + JavaScript
- REST API oparte na Flask

## Technologie

- Python (Flask, SQLAlchemy, Flask-Migrate, Flask-CORS)
- HTML, JavaScript
- Pytest, pytest-flask
- GitHub Actions (CI)
- Docker (uruchomienie lokalne)

## Automatyzacja

- Testy jednostkowe z Pytest
- Automatyczne testy i budowanie przez GitHub Actions
- Walidacja wiadomości commitów i nazw branchy
- Zabezpieczenia branchy (branch protection rules)

## Uruchomienie lokalne (Docker)

```bash
docker build -t habit-tracker .
docker run -p 5000:5000 habit-tracker
