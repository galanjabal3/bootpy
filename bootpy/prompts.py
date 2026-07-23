import re

from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()

def validate_project_name(name: str) -> bool:
    # Must be valid identifier containing only alphanumeric, underscores, or hyphens
    if not name:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))

def get_scaffold_answers() -> dict:
    console.print("\n[bold cyan]🔧 Project Configuration[/bold cyan]")

    # 1. Project Name
    while True:
        project_name = Prompt.ask("[yellow]Enter project name[/yellow]", default="my-project")
        if validate_project_name(project_name):
            break
        console.print("[red]Invalid project name. Use only alphanumeric characters, underscores, or hyphens.[/red]")

    # 2. Framework
    framework = Prompt.ask(
        "[yellow]Choose Python framework[/yellow]",
        choices=["FastAPI", "Django"],
        default="FastAPI"
    )

    # 3. Database
    database = Prompt.ask(
        "[yellow]Choose database[/yellow]",
        choices=["SQLite", "PostgreSQL"],
        default="SQLite"
    )

    # 4. Docker
    docker = Confirm.ask("[yellow]Include Docker & Docker Compose setup?[/yellow]", default=True)

    # 5. Pytest
    pytest = Confirm.ask("[yellow]Include Pytest testing setup?[/yellow]", default=True)

    # Framework-specific options
    answers = {
        "project_name": project_name,
        "framework": framework,
        "database": database,
        "docker": docker,
        "pytest": pytest
    }

    if framework == "FastAPI":
        console.print("\n[bold cyan]⚡ FastAPI Specific Options[/bold cyan]")
        answers["async_orm"] = Confirm.ask("[yellow]Include Async ORM (SQLAlchemy async)?[/yellow]", default=True)
        answers["auth_jwt"] = Confirm.ask("[yellow]Include JWT Authentication boilerplate?[/yellow]", default=True)
    elif framework == "Django":
        console.print("\n[bold cyan]🛡️ Django Specific Options[/bold cyan]")
        answers["django_admin"] = Confirm.ask("[yellow]Include Django Admin Panel?[/yellow]", default=True)
        answers["drf"] = Confirm.ask("[yellow]Include Django REST Framework (DRF)?[/yellow]", default=True)

    return answers
