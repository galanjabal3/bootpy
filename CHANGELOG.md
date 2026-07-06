# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-06

### Added
- Interactive CLI using Typer and Rich with ASCII banner
- Multi-framework support: **FastAPI** and **Django**
- Jinja2-powered conditional template rendering engine
- FastAPI template includes:
  - Async SQLAlchemy ORM (optional)
  - JWT Authentication with `python-jose` and `passlib` (optional)
  - Docker & Docker Compose (optional)
  - Pytest setup with `httpx` (optional)
  - Full project structure: `app/api/`, `app/core/`, `app/db/`, `app/models/`, `app/schemas/`
- Django template includes:
  - Admin panel toggle (optional)
  - Django REST Framework with `ModelViewSet` and serializers (optional)
  - `django-environ` for environment-based settings
  - Docker & Docker Compose (optional)
  - Pytest with `pytest-django` (optional)
  - Core app with `Item` model and health check endpoint
- Universal options: database choice (SQLite / PostgreSQL), Docker, Pytest
- Auto project name → Python package name conversion (e.g. `my-app` → `my_app`)
- Unit tests covering FastAPI and Django generation flows
- GitHub Actions CI workflow for Python 3.9, 3.10, 3.11
