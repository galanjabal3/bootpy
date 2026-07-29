import os
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bootpy import __version__
from bootpy.generator import generate_project
from bootpy.prompts import get_scaffold_answers

app = typer.Typer(help="bootpy: Interactive Python Project Scaffolding CLI Tool")
console = Console()

BANNER = """
 [bold cyan] _                 _               [/bold cyan]
 [bold cyan]| |               | |              [/bold cyan]
 [bold cyan]| |__   ___   ___ | |_ _ __  _   _ [/bold cyan]
 [bold cyan]| '_ \\ / _ \\ / _ \\| __| '_ \\| | | |[/bold cyan]
 [bold cyan]| |_) | (_) | (_) | |_| |_) | |_| |[/bold cyan]
 [bold cyan]|_.__/ \\___/ \\___/ \\__| .__/ \\__, |[/bold cyan]
 [bold cyan]                      | |     __/ |[/bold cyan]
 [bold cyan]                      |_|    |___/ [/bold cyan]
"""

FRAMEWORKS = {
    "fastapi": {"name": "FastAPI", "files": 19},
    "django": {"name": "Django", "files": 21},
    "flask": {"name": "Flask", "files": 18},
}

def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]bootpy[/bold cyan] version [bold]{__version__}[/bold]")
        raise typer.Exit()

def get_templates_dir() -> str:
    """Return the path to the templates directory."""
    return os.path.join(os.path.dirname(__file__), "templates")

def _generate(target_path: str, answers: dict):
    """Common generation logic for both interactive and non-interactive modes."""
    if os.path.exists(target_path) and os.listdir(target_path):
        console.print(f"\n[bold red]Error: Target directory '{target_path}' already exists and is not empty.[/bold red]")
        raise typer.Exit(code=1)

    console.print(f"\n[yellow]Generating project in [bold]{target_path}[/bold]...[/yellow]")

    generate_project(target_path, answers)

    console.print("\n[bold green]🚀 Project scaffolded successfully![/bold green]")

    instructions = f"""
To get started:
  [bold cyan]cd {answers['project_name']}[/bold cyan]
  [bold cyan]python3 -m venv .venv[/bold cyan]
  [bold cyan]source .venv/bin/activate[/bold cyan]
  [bold cyan]pip install -r requirements.txt[/bold cyan]
"""
    if answers.get("docker"):
        instructions += "  [bold cyan]docker-compose up --build[/bold cyan] (to run inside containers)\n"

    console.print(Panel(
        instructions.strip(),
        title="[bold green]Next Steps[/bold green]",
        expand=False
    ))

@app.command()
def create(
    name: str = typer.Argument(help="Project name"),
    framework: str = typer.Option("fastapi", "--framework", "-f", help="Python framework (fastapi/django/flask)"),
    database: str = typer.Option("sqlite", "--database", "-d", help="Database (sqlite/postgres)"),
    docker: bool = typer.Option(True, "--docker/--no-docker", help="Include Docker setup"),
    pytest: bool = typer.Option(True, "--pytest/--no-pytest", help="Include Pytest setup"),
    jwt: bool = typer.Option(True, "--jwt/--no-jwt", help="Include JWT auth (FastAPI/Flask only)"),
    async_orm: bool = typer.Option(True, "--async-orm/--no-async-orm", help="Include Async ORM (FastAPI only)"),
    django_admin: bool = typer.Option(True, "--django-admin/--no-django-admin", help="Include Django Admin (Django only)"),
    drf: bool = typer.Option(True, "--drf/--no-drf", help="Include DRF (Django only)"),
    output_dir: str = typer.Option(".", "--output-dir", "-o", help="Output directory"),
):
    """
    Create a new Python project (non-interactive mode).

    Example:

      bootpy create my-api --framework fastapi --database postgres --jwt
    """
    console.print(BANNER)

    # Validate framework
    framework_lower = framework.lower()
    if framework_lower not in FRAMEWORKS:
        console.print(f"[bold red]Error: Invalid framework '{framework}'. Choose: fastapi, django, flask[/bold red]")
        raise typer.Exit(code=1)

    # Validate database
    database_lower = database.lower()
    if database_lower not in ("sqlite", "postgres"):
        console.print(f"[bold red]Error: Invalid database '{database}'. Choose: sqlite, postgres[/bold red]")
        raise typer.Exit(code=1)

    # Build answers dict
    answers = {
        "project_name": name,
        "framework": FRAMEWORKS[framework_lower]["name"],
        "database": "PostgreSQL" if database_lower == "postgres" else "SQLite",
        "docker": docker,
        "pytest": pytest,
    }

    # Framework-specific options
    if framework_lower == "fastapi":
        answers["async_orm"] = async_orm
        answers["auth_jwt"] = jwt
    elif framework_lower == "django":
        answers["django_admin"] = django_admin
        answers["drf"] = drf

    target_path = os.path.abspath(os.path.join(output_dir, name))

    try:
        _generate(target_path, answers)
    except KeyboardInterrupt:
        console.print("\n[yellow]Scaffolding cancelled by user.[/yellow]")
        raise typer.Exit(code=0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred during scaffolding: {e}[/bold red]")
        raise typer.Exit(code=1)

@app.command()
def list():
    """
    List all available templates.
    """
    console.print(BANNER)

    table = Table(title="Available Templates", show_header=True, header_style="bold cyan")
    table.add_column("Framework", style="bold")
    table.add_column("Files", justify="right")
    table.add_column("Features")

    table.add_row(
        "FastAPI",
        "19",
        "Async ORM, JWT Auth, Docker, Pytest"
    )
    table.add_row(
        "Django",
        "21",
        "Admin Panel, DRF, Docker, Pytest"
    )
    table.add_row(
        "Flask",
        "18",
        "SQLAlchemy, JWT Auth, Docker, Pytest"
    )

    console.print(table)
    console.print("\n[dim]Use 'bootpy create <name> --framework <framework>' to scaffold.[/dim]")

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the installed version and exit."
    ),
    output_dir: str = typer.Option(
        ".",
        "--output-dir",
        "-o",
        help="Directory where the project should be created."
    )
):
    """
    Interactive scaffolding tool to kickstart your next Python project (FastAPI / Django).
    """
    # If a subcommand is invoked, skip interactive mode
    if ctx.invoked_subcommand is not None:
        return

    console.print(BANNER)
    console.print("[bold white]Welcome to bootpy! Let's scaffold your project.[/bold white]\n")

    try:
        answers = get_scaffold_answers()

        target_path = os.path.abspath(os.path.join(output_dir, answers["project_name"]))

        _generate(target_path, answers)

    except KeyboardInterrupt:
        console.print("\n[yellow]Scaffolding cancelled by user.[/yellow]")
        raise typer.Exit(code=0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred during scaffolding: {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
