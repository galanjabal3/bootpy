import os
import tempfile

import pytest

from bootpy.generator import generate_project
from bootpy.prompts import validate_project_name


def test_fastapi_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "my-fastapi-app",
            "framework": "FastAPI",
            "database": "SQLite",
            "docker": True,
            "pytest": True,
            "async_orm": True,
            "auth_jwt": True
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        # Verify files are created
        assert os.path.exists(os.path.join(target_path, "README.md"))
        assert os.path.exists(os.path.join(target_path, "requirements.txt"))
        assert os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert os.path.exists(os.path.join(target_path, "docker-compose.yml"))
        assert os.path.exists(os.path.join(target_path, "app", "main.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "config.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "security.py"))
        assert os.path.exists(os.path.join(target_path, "app", "db", "session.py"))
        assert os.path.exists(os.path.join(target_path, "app", "models", "user.py"))
        assert os.path.exists(os.path.join(target_path, "app", "schemas", "user.py"))
        assert os.path.exists(os.path.join(target_path, "app", "api", "router.py"))
        assert os.path.exists(os.path.join(target_path, "app", "api", "endpoints", "auth.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "test_main.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "test_auth.py"))

def test_django_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "my-django-app",
            "framework": "Django",
            "database": "PostgreSQL",
            "docker": True,
            "pytest": True,
            "django_admin": True,
            "drf": True
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        package_name = "my_django_app"

        # Verify files are created
        assert os.path.exists(os.path.join(target_path, "README.md"))
        assert os.path.exists(os.path.join(target_path, "requirements.txt"))
        assert os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert os.path.exists(os.path.join(target_path, "docker-compose.yml"))
        assert os.path.exists(os.path.join(target_path, "manage.py"))
        assert os.path.exists(os.path.join(target_path, package_name, "settings.py"))
        assert os.path.exists(os.path.join(target_path, package_name, "urls.py"))
        assert os.path.exists(os.path.join(target_path, "core", "models.py"))
        assert os.path.exists(os.path.join(target_path, "core", "serializers.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "test_models.py"))
        assert os.path.exists(os.path.join(target_path, "pytest.ini"))

def test_invalid_framework():
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "invalid-project",
            "framework": "NonExistentFramework",
            "database": "SQLite",
            "docker": False,
            "pytest": False
        }

        target_path = os.path.join(tmpdir, answers["project_name"])

        # Generator should raise ValueError for invalid framework
        with pytest.raises(ValueError, match="Template directory for framework 'nonexistentframework' not found."):
            generate_project(target_path, answers)

        # Ensure target directory was not created (rollback functionality)
        assert not os.path.exists(target_path)


# --- Negative Case Tests ---

def test_fastapi_without_docker_and_auth():
    """Optional files must NOT be generated when user opts out."""
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "minimal-fastapi",
            "framework": "FastAPI",
            "database": "SQLite",
            "docker": False,
            "pytest": False,
            "async_orm": False,
            "auth_jwt": False
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        # Core files should still exist
        assert os.path.exists(os.path.join(target_path, "README.md"))
        assert os.path.exists(os.path.join(target_path, "requirements.txt"))
        assert os.path.exists(os.path.join(target_path, "app", "main.py"))

        # Docker files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert not os.path.exists(os.path.join(target_path, "docker-compose.yml"))

        # Auth files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "app", "core", "security.py"))
        assert not os.path.exists(os.path.join(target_path, "app", "api", "endpoints", "auth.py"))
        assert not os.path.exists(os.path.join(target_path, "app", "models", "user.py"))
        assert not os.path.exists(os.path.join(target_path, "app", "schemas", "token.py"))

        # ORM / DB files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "app", "db", "session.py"))
        assert not os.path.exists(os.path.join(target_path, "app", "db", "base.py"))

        # Pytest files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert not os.path.exists(os.path.join(target_path, "tests", "test_main.py"))


def test_django_without_docker_and_drf():
    """Optional Django files must NOT be generated when user opts out."""
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "minimal-django",
            "framework": "Django",
            "database": "SQLite",
            "docker": False,
            "pytest": False,
            "django_admin": True,
            "drf": False
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        package_name = "minimal_django"

        # Core files should still exist
        assert os.path.exists(os.path.join(target_path, "manage.py"))
        assert os.path.exists(os.path.join(target_path, package_name, "settings.py"))
        assert os.path.exists(os.path.join(target_path, "core", "models.py"))

        # Docker files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert not os.path.exists(os.path.join(target_path, "docker-compose.yml"))

        # DRF file must NOT exist
        assert not os.path.exists(os.path.join(target_path, "core", "serializers.py"))

        # Pytest files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "tests", "test_models.py"))
        assert not os.path.exists(os.path.join(target_path, "tests", "test_views.py"))


# --- validate_project_name Tests ---

def test_valid_project_names():
    assert validate_project_name("my-project") is True
    assert validate_project_name("my_project") is True
    assert validate_project_name("MyProject123") is True
    assert validate_project_name("a") is True


def test_invalid_project_names():
    assert validate_project_name("") is False
    assert validate_project_name("my project") is False   # spasi tidak diizinkan
    assert validate_project_name("proj@123") is False     # karakter spesial
    assert validate_project_name("proj/sub") is False     # slash tidak diizinkan
    assert validate_project_name("proj.name") is False    # titik tidak diizinkan

