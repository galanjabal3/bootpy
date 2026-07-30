# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-29

### Added
- **Litestar** framework support with 17 template files
  - App factory pattern
  - SQLAlchemy async ORM
  - DTOs (Data Transfer Objects)
  - Dependency Injection
  - JWT Authentication (optional)
  - Docker & Docker Compose (optional)
  - Pytest setup with async support (optional)
- **Custom templates support**: `bootpy create my-api --template ./my-template/`
  - Load templates from any directory
  - Manifest.json support for skip logic
  - Full Jinja2 rendering
- Litestar-specific options in interactive mode
- Unit tests for Litestar generation, custom templates, and negative cases

### Changed
- Framework validation updated to include Litestar
- Non-interactive mode now supports `--template` option
- CLI help text updated with all 4 frameworks

## [0.2.1] - 2026-07-29

### Fixed
- Rebuild package with updated README.md (Flask + non-interactive mode description)

## [0.2.0] - 2026-07-27

### Added
- Non-interactive mode: `bootpy create <name> --framework <fw> --database <db>` for CI/CD and automation
- `bootpy list` command to display all available templates
- **Flask** framework support with 18 template files
  - App factory pattern
  - SQLAlchemy ORM
  - JWT Authentication (optional)
  - Docker & Docker Compose (optional)
  - Pytest setup (optional)
- Flask-specific options in interactive mode
- Unit tests for Flask generation and negative cases

### Changed
- CLI restructured with subcommands (`create`, `list`)
- Interactive mode now runs as default callback (no subcommand required)
- Framework validation updated to include Flask

## [0.1.3] - 2026-07-23

### Fixed
- Remove dead code: `if rel_root == "manifest.json"` in `generator.py` (condition was never reachable since `os.walk` yields directories, not files)
- Refactor `should_skip_path()` to eliminate double negation — logic is now consistent with `should_skip_file()`
- Remove orphan dependency `questionary` from `pyproject.toml` and `requirements.txt` (library was never imported)
- Remove legacy `setup.py` (fully superseded by `pyproject.toml`)

### Added
- Ruff linter (`ruff>=0.5.0`) added to dev dependencies (`requirements-dev.txt`) and CI pipeline
- Python 3.12 added to CI test matrix
- Negative case tests: verify optional files are **not** generated when user opts out (Docker, JWT Auth, Async ORM, DRF, Pytest)
- Unit tests for `validate_project_name()` covering valid and invalid input patterns

## [0.1.1] - 2026-07-07


### Fixed
- Template files (`.jinja`) were not included when the package was installed via pip
  (e.g. `pip install git+https://...`), causing scaffolding to fail with
  `Template directory for framework 'fastapi' not found`.
- Added `include-package-data` and `package-data` configuration in `pyproject.toml`
  so all template files under `bootpy/templates/` are correctly bundled into the
  built wheel/sdist.

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
