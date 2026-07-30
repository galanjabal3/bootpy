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

def test_flask_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "my-flask-app",
            "framework": "Flask",
            "database": "SQLite",
            "docker": True,
            "pytest": True,
            "auth_jwt": True
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        # Verify files are created
        assert os.path.exists(os.path.join(target_path, "README.md"))
        assert os.path.exists(os.path.join(target_path, "requirements.txt"))
        assert os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert os.path.exists(os.path.join(target_path, "docker-compose.yml"))
        assert os.path.exists(os.path.join(target_path, ".env"))
        assert os.path.exists(os.path.join(target_path, "app", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "config.py"))
        assert os.path.exists(os.path.join(target_path, "app", "models", "user.py"))
        assert os.path.exists(os.path.join(target_path, "app", "routes", "main.py"))
        assert os.path.exists(os.path.join(target_path, "app", "routes", "auth.py"))
        assert os.path.exists(os.path.join(target_path, "app", "services", "user_service.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "test_main.py"))

def test_litestar_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "my-litestar-app",
            "framework": "Litestar",
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
        assert os.path.exists(os.path.join(target_path, ".env"))
        assert os.path.exists(os.path.join(target_path, "app", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "controllers", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "dto", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "models", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "services", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert os.path.exists(os.path.join(target_path, "tests", "test_main.py"))

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


def test_flask_without_docker_and_auth():
    """Optional Flask files must NOT be generated when user opts out."""
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "minimal-flask",
            "framework": "Flask",
            "database": "SQLite",
            "docker": False,
            "pytest": False,
            "auth_jwt": False
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        # Core files should still exist
        assert os.path.exists(os.path.join(target_path, "README.md"))
        assert os.path.exists(os.path.join(target_path, "requirements.txt"))
        assert os.path.exists(os.path.join(target_path, "app", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "config.py"))
        assert os.path.exists(os.path.join(target_path, "app", "routes", "main.py"))

        # Docker files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert not os.path.exists(os.path.join(target_path, "docker-compose.yml"))

        # Auth files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "app", "routes", "auth.py"))

        # Pytest files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert not os.path.exists(os.path.join(target_path, "tests", "test_main.py"))


def test_litestar_without_docker_and_auth():
    """Optional Litestar files must NOT be generated when user opts out."""
    with tempfile.TemporaryDirectory() as tmpdir:
        answers = {
            "project_name": "minimal-litestar",
            "framework": "Litestar",
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
        assert os.path.exists(os.path.join(target_path, "app", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "core", "__init__.py"))
        assert os.path.exists(os.path.join(target_path, "app", "controllers", "__init__.py"))

        # Docker files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "Dockerfile"))
        assert not os.path.exists(os.path.join(target_path, "docker-compose.yml"))

        # Pytest files must NOT exist
        assert not os.path.exists(os.path.join(target_path, "tests", "conftest.py"))
        assert not os.path.exists(os.path.join(target_path, "tests", "test_main.py"))


# --- Custom Template Tests ---

def test_custom_template():
    """Custom template should work correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom template
        custom_template_dir = os.path.join(tmpdir, "custom-template")
        os.makedirs(custom_template_dir)

        # Create manifest.json
        manifest = {"skip_files": {}}
        with open(os.path.join(custom_template_dir, "manifest.json"), "w") as f:
            import json
            json.dump(manifest, f)

        # Create a simple template file
        with open(os.path.join(custom_template_dir, "README.md.jinja"), "w") as f:
            f.write("# {{ project_name }}\n\nCustom template.")

        answers = {
            "project_name": "my-custom-app",
            "framework": "custom",
            "database": "SQLite",
            "docker": False,
            "pytest": False,
            "custom_template": custom_template_dir,
        }

        target_path = os.path.join(tmpdir, answers["project_name"])
        generate_project(target_path, answers)

        # Verify files are created
        assert os.path.exists(os.path.join(target_path, "README.md"))

        # Check content
        with open(os.path.join(target_path, "README.md")) as f:
            content = f.read()
            assert "my-custom-app" in content
            assert "Custom template." in content


def test_custom_template_missing_manifest():
    """Custom template without manifest.json should raise error."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a custom template without manifest.json
        custom_template_dir = os.path.join(tmpdir, "custom-template")
        os.makedirs(custom_template_dir)

        # Create a simple template file
        with open(os.path.join(custom_template_dir, "README.md.jinja"), "w") as f:
            f.write("# {{ project_name }}")

        answers = {
            "project_name": "my-custom-app",
            "framework": "custom",
            "database": "SQLite",
            "docker": False,
            "pytest": False,
            "custom_template": custom_template_dir,
        }

        target_path = os.path.join(tmpdir, answers["project_name"])

        # Should work even without manifest.json (uses default empty manifest)
        generate_project(target_path, answers)
        assert os.path.exists(os.path.join(target_path, "README.md"))


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

