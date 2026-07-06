import os
import shutil
from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()

def get_templates_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "templates")

def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def generate_project(target_dir: str, answers: dict):
    ensure_directory(target_dir)
    
    # Initialize Jinja environment
    templates_dir = get_templates_dir()
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        keep_trailing_newline=True
    )
    
    framework = answers["framework"].lower()  # "fastapi" or "django"
    framework_template_dir = os.path.join(templates_dir, framework)
    
    # Check if template directory exists
    if not os.path.exists(framework_template_dir):
        raise ValueError(f"Template directory for framework '{framework}' not found.")
        
    # We will walk through the framework template directory and render files
    for root, dirs, files in os.walk(framework_template_dir):
        # Calculate relative path to framework template dir
        rel_root = os.path.relpath(root, framework_template_dir)
        
        # Decide if we skip this directory/path based on answers
        if should_skip_path(rel_root, answers):
            continue
            
        # Target directory to create
        target_root = target_dir if rel_root == "." else os.path.join(target_dir, rel_root)
        
        # We might need to rename the main project folder in Django or package names
        # For Django, we rename the 'myproject' folder to the actual project name
        if framework == "django" and "myproject" in rel_root:
            proj_name = answers["project_name"].replace("-", "_") # Python package name friendly
            new_rel_root = rel_root.replace("myproject", proj_name)
            target_root = os.path.join(target_dir, new_rel_root)

        ensure_directory(target_root)
        
        for file in files:
            template_file_path = os.path.join(rel_root, file) if rel_root != "." else file
            
            if should_skip_file(template_file_path, answers):
                continue
                
            # Determine target filename (strip .jinja extension)
            target_file_name = file
            if file.endswith(".jinja"):
                target_file_name = file[:-6]
                
            # Django specific folder rename for config file outputs
            if framework == "django" and "myproject" in target_file_name:
                proj_name = answers["project_name"].replace("-", "_")
                target_file_name = target_file_name.replace("myproject", proj_name)
                
            target_file_path = os.path.join(target_root, target_file_name)
            
            # Render and write template
            template_name = f"{framework}/{template_file_path}"
            template = env.get_template(template_name)
            
            # Prepare context for rendering
            context = answers.copy()
            # Add package-safe name
            context["package_name"] = answers["project_name"].replace("-", "_")
            
            content = template.render(**context)
            
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            console.print(f"  [green]✓[/green] Created {os.path.relpath(target_file_path, target_dir)}")

def should_skip_path(rel_path: str, answers: dict) -> bool:
    if rel_path == ".":
        return False
        
    parts = rel_path.split(os.sep)
    
    # FastAPI specific filters
    if answers["framework"] == "FastAPI":
        if "db" in parts and not answers.get("async_orm", False):
            return True
        if "tests" in parts and not answers.get("pytest", False):
            return True
            
    # Django specific filters
    elif answers["framework"] == "Django":
        if "tests" in parts and not answers.get("pytest", False):
            return True
            
    return False

def should_skip_file(rel_file_path: str, answers: dict) -> bool:
    parts = rel_file_path.split(os.sep)
    filename = parts[-1]
    
    # Universal file checks
    if "Dockerfile" in filename or "docker-compose" in filename:
        if not answers.get("docker", False):
            return True
            
    # FastAPI specific checks
    if answers["framework"] == "FastAPI":
        is_auth = answers.get("auth_jwt", False)
        is_orm = answers.get("async_orm", False)
        
        if "security.py" in filename and not is_auth:
            return True
        if "auth.py" in filename and not is_auth:
            return True
        if "user.py" in filename and not is_auth:
            return True
        if "token.py" in filename and not is_auth:
            return True
        if "test_auth.py" in filename and not is_auth:
            return True
        if "session.py" in filename and not is_orm:
            return True
        if "base.py" in filename and not is_orm:
            return True
            
    # Django specific checks
    elif answers["framework"] == "Django":
        is_drf = answers.get("drf", False)
        
        if "serializers.py" in filename and not is_drf:
            return True
            
    return False
