import json
import os
import shutil
import tempfile

from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()

def get_templates_dir() -> str:
    """Return the path to the templates directory."""
    return os.path.join(os.path.dirname(__file__), "templates")

def ensure_directory(path: str):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def load_manifest(framework: str):
    """Load the manifest.json for a given framework."""
    manifest_path = os.path.join(get_templates_dir(), framework, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            return json.load(f)
    return {"skip_paths": {}, "skip_files": {}}

def check_condition(condition: str, answers: dict) -> bool:
    """Evaluate skip conditions from the manifest."""
    if condition.startswith("not "):
        key = condition[4:]
        return not answers.get(key, False)
    return answers.get(condition, False)

def generate_project(target_dir: str, answers: dict):
    """Generate the project structure using templates."""
    # Use a staging directory for atomicity
    staging_dir = tempfile.mkdtemp()

    try:
        project_staging_dir = os.path.join(staging_dir, answers["project_name"])

        # Check if using custom template
        custom_template = answers.get("custom_template")
        if custom_template:
            templates_dir = custom_template
            framework = "custom"
        else:
            templates_dir = get_templates_dir()
            framework = answers["framework"].lower()

        # Initialize Jinja environment
        env = Environment(
            loader=FileSystemLoader(templates_dir),
            keep_trailing_newline=True
        )

        if custom_template:
            framework_template_dir = custom_template
            manifest_path = os.path.join(custom_template, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path) as f:
                    manifest = json.load(f)
            else:
                manifest = {"skip_paths": {}, "skip_files": {}}
        else:
            framework_template_dir = os.path.join(templates_dir, framework)
            manifest = load_manifest(framework)

        # Check if template directory exists
        if not os.path.exists(framework_template_dir):
            raise ValueError(f"Template directory for framework '{framework}' not found.")

        # Walk through the framework template directory and render files
        for root, dirs, files in os.walk(framework_template_dir):
            # Calculate relative path to framework template dir
            rel_root = os.path.relpath(root, framework_template_dir)

            # Decide if we skip this directory/path based on manifest
            if should_skip_path(rel_root, manifest, answers):
                continue

            # Determine staging path
            current_staging_path = project_staging_dir
            if rel_root != ".":
                # Handle Django project rename logic
                final_rel_root = rel_root
                if framework == "django" and "myproject" in rel_root:
                    proj_name = answers["project_name"].replace("-", "_")
                    final_rel_root = rel_root.replace("myproject", proj_name)

                current_staging_path = os.path.join(project_staging_dir, final_rel_root)

            ensure_directory(current_staging_path)

            for file in files:
                if file == "manifest.json":
                    continue

                # Determine target filename
                target_file_name = file
                if file.endswith(".jinja"):
                    target_file_name = file[:-6]

                # Check skip using processed filename or relative path
                template_file_path = os.path.join(rel_root, file) if rel_root != "." else file

                # IMPORTANT: Skip logic check
                if should_skip_file(template_file_path, manifest, answers) or \
                   should_skip_file(target_file_name, manifest, answers):
                    continue

                # Django specific: rename 'myproject' in filenames
                if framework == "django" and "myproject" in target_file_name:
                    proj_name = answers["project_name"].replace("-", "_")
                    target_file_name = target_file_name.replace("myproject", proj_name)

                target_file_path = os.path.join(current_staging_path, target_file_name)

                # Render and write template
                if custom_template:
                    template_name = template_file_path
                else:
                    template_name = f"{framework}/{template_file_path}"
                template = env.get_template(template_name)

                context = answers.copy()
                context["package_name"] = answers["project_name"].replace("-", "_")

                content = template.render(**context)

                with open(target_file_path, "w", encoding="utf-8") as f:
                    f.write(content)

        # If everything succeeded, move the staged project to the final target_dir
        shutil.move(project_staging_dir, target_dir)
        console.print(f"  [green]✓[/green] Project successfully generated in {target_dir}")

    finally:
        # Cleanup staging directory
        shutil.rmtree(staging_dir)

def should_skip_path(rel_path: str, manifest: dict, answers: dict) -> bool:
    """Check if a path should be skipped.

    A path is skipped when its manifest condition evaluates to True.
    Conditions starting with 'not ' are already handled by check_condition.
    """
    if rel_path == ".":
        return False

    for path, condition in manifest.get("skip_paths", {}).items():
        # Check if manifest path is a parent directory or the path itself
        if rel_path.startswith(path):
            if check_condition(condition, answers):
                return True
    return False

def should_skip_file(rel_file_path: str, manifest: dict, answers: dict) -> bool:
    """Check if a file should be skipped."""
    # Check if the full relative path is in manifest skip list
    for path, condition in manifest.get("skip_files", {}).items():
        # Match if filename or relative path is in skip list
        if rel_file_path == path or os.path.basename(rel_file_path) == path:
            # Check condition. If condition is True (meaning we skip), return True.
            if check_condition(condition, answers):
                return True
    return False
