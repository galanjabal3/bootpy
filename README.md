# bootpy 🐍

> **Interactive multi-framework Python scaffolding CLI** — scaffold a production-ready FastAPI or Django project in under 60 seconds.

[![CI](https://github.com/galanjabal3/bootpy/actions/workflows/ci.yml/badge.svg)](https://github.com/galanjabal3/bootpy/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/bootpy-cli)](https://pypi.org/project/bootpy-cli/)

---

## ✨ Why bootpy?

Every Python scaffolding tool I found was **single-framework** — either FastAPI-only or Django-only. `bootpy` is the first CLI that lets you pick your framework interactively, while generating a fully opinionated, production-ready structure with your exact configuration.

Think `create-react-app`, but for Python backend projects.

---

## 🚀 Quick Start

```bash
pip install bootpy-cli
bootpy
```

Follow the interactive prompts:

```
🔧 Project Configuration
Enter project name: my-api
Choose Python framework [FastAPI/Django]: FastAPI
Choose database [SQLite/PostgreSQL]: PostgreSQL
Include Docker & Docker Compose setup? [y/n]: y
Include Pytest testing setup? [y/n]: y

⚡ FastAPI Specific Options
Include Async ORM (SQLAlchemy async)? [y/n]: y
Include JWT Authentication boilerplate? [y/n]: y

Generating project in /path/to/my-api...
  ✓ Created app/main.py
  ✓ Created app/core/config.py
  ✓ Created app/core/security.py
  ✓ Created app/db/session.py
  ... (19 files total)

🚀 Project scaffolded successfully!
```

---

## ⚙️ Configuration Options

### Universal (all frameworks)

| Option | Choices | Default |
|---|---|---|
| Project name | Any alphanumeric + `-_` | `my-project` |
| Framework | `FastAPI`, `Django` | `FastAPI` |
| Database | `SQLite`, `PostgreSQL` | `SQLite` |
| Docker & Docker Compose | `y/n` | `y` |
| Pytest setup | `y/n` | `y` |

### FastAPI-specific

| Option | Choices | Default |
|---|---|---|
| Async ORM (SQLAlchemy 2.0) | `y/n` | `y` |
| JWT Authentication | `y/n` | `y` |

### Django-specific

| Option | Choices | Default |
|---|---|---|
| Django Admin panel | `y/n` | `y` |
| Django REST Framework | `y/n` | `y` |

---

## 📁 Generated Project Structure

### FastAPI (full options)

```
my-api/
├── app/
│   ├── main.py                    # FastAPI app + startup events
│   ├── api/
│   │   ├── router.py              # Central API router
│   │   └── endpoints/
│   │       ├── auth.py            # JWT login endpoint
│   │       └── users.py           # User CRUD with auth
│   ├── core/
│   │   ├── config.py              # Pydantic settings
│   │   └── security.py            # JWT + bcrypt utilities
│   ├── db/
│   │   ├── session.py             # Async SQLAlchemy engine
│   │   └── base.py                # Declarative Base
│   ├── models/
│   │   └── user.py                # SQLAlchemy User model
│   └── schemas/
│       ├── user.py                # Pydantic User schemas
│       └── token.py               # Token schemas
├── tests/
│   ├── conftest.py                # Pytest fixtures + AsyncClient
│   ├── test_main.py
│   └── test_auth.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

### Django (full options)

```
my-django-project/
├── my_django_project/             # Django project package
│   ├── settings.py                # django-environ based settings
│   ├── urls.py                    # Root URL config (admin + API)
│   ├── wsgi.py
│   └── asgi.py
├── core/                          # Core Django app
│   ├── models.py                  # Item model
│   ├── views.py                   # Health check + DRF ViewSet
│   ├── serializers.py             # DRF ModelSerializer
│   ├── urls.py                    # App URL config
│   └── apps.py
├── tests/
│   ├── test_models.py
│   └── test_views.py
├── manage.py
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Tech Stack

| Purpose | Library |
|---|---|
| CLI framework | [Typer](https://typer.tiangolo.com/) |
| Terminal UI | [Rich](https://github.com/Textualize/rich) |
| Template rendering | [Jinja2](https://jinja.palletsprojects.com/) |
| Distribution | [PyPI](https://pypi.org/) |

---

## 🔧 Development Setup

```bash
git clone https://github.com/galanjabal3/bootpy
cd bootpy

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

# Run tests
pytest

# Run CLI from source
bootpy
```

---

## 🧠 Design Decisions

### Why FastAPI + Django as the first two frameworks?

FastAPI and Django represent **the most contrasting philosophies** in Python backend development:
- **FastAPI**: async-first, type-hint driven, OpenAPI auto-generation, minimal structure
- **Django**: synchronous ORM, batteries-included, admin panel, opinionated structure

Supporting both frameworks in one CLI requires understanding that their project structures are fundamentally different — not just in syntax but in philosophy. This was intentional: it tells a stronger architecture story than a single-framework tool would.

Flask was skipped for v1 because its minimalism means the scaffold would be nearly identical to a FastAPI base structure with fewer features. It's a natural v2 candidate.

### Why Jinja2 for templating instead of string interpolation?

Conditional file generation (e.g., skip `session.py` if no ORM, skip `security.py` if no JWT) requires a proper templating engine. Jinja2 allows both **conditional blocks** within files and **conditional inclusion** of entire files — which plain string interpolation can't do cleanly.

### Why the conditional file-skip logic in `generator.py` instead of the templates?

Keeping the skip logic in Python (`generator.py`) rather than spreading guards across every template keeps templates **clean and readable**, easier to extend, and decoupled from generation logic.

---

## 📄 License

MIT — see [LICENSE](LICENSE)
