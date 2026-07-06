import os
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from bootpy import __version__
from bootpy.prompts import get_scaffold_answers
from bootpy.generator import generate_project

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

def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]bootpy[/bold cyan] version [bold]{__version__}[/bold]")
        raise typer.Exit()

@app.command()
def main(
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
    console.print(BANNER)
    console.print("[bold white]Welcome to bootpy! Let's scaffold your project.[/bold white]\n")
    
    try:
        answers = get_scaffold_answers()
        
        target_path = os.path.abspath(os.path.join(output_dir, answers["project_name"]))
        
        # Check if directory already exists and is not empty
        if os.path.exists(target_path) and os.listdir(target_path):
            console.print(f"\n[bold red]Error: Target directory '{target_path}' already exists and is not empty.[/bold red]")
            raise typer.Exit(code=1)
            
        console.print(f"\n[yellow]Generating project in [bold]{target_path}[/bold]...[/yellow]")
        
        # Call generator
        generate_project(target_path, answers)
        
        # Display Success Message
        console.print("\n[bold green]🚀 Project scaffolded successfully![/bold green]")
        
        instructions = f"""
To get started:
  [bold cyan]cd {answers['project_name']}[/bold cyan]
  [bold cyan]python3 -m venv .venv[/bold cyan]
  [bold cyan]source .venv/bin/activate[/bold cyan]
  [bold cyan]pip install -r requirements.txt[/bold cyan]
"""
        if answers["docker"]:
            instructions += "  [bold cyan]docker-compose up --build[/bold cyan] (to run inside containers)\n"
            
        console.print(Panel(
            instructions.strip(),
            title="[bold green]Next Steps[/bold green]",
            expand=False
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Scaffolding cancelled by user.[/yellow]")
        raise typer.Exit(code=0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred during scaffolding: {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
