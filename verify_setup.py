#!/usr/bin/env python3
"""Verification script to check if the application is properly set up."""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"{status} {description}: {filepath}")
    return exists


def check_directory_exists(dirpath: str, description: str) -> bool:
    """Check if a directory exists."""
    exists = Path(dirpath).is_dir()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    print(f"{status} {description}: {dirpath}")
    return exists


def check_env_file() -> bool:
    """Check if .env file exists and has required variables."""
    print(f"\n{YELLOW}Checking Environment Configuration...{RESET}")
    
    env_file = Path(".env")
    if not env_file.exists():
        print(f"{RED}✗{RESET} .env file not found. Copy .env.example to .env")
        return False
    
    print(f"{GREEN}✓{RESET} .env file exists")
    
    # Check for required variables
    required_vars = [
        "SECRET_KEY",
        "DATABASE_URL",
        "OPENAI_API_KEY",
    ]
    
    with open(env_file) as f:
        content = f.read()
        
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
        elif "placeholder" in content.split(var)[1].split('\n')[0].lower():
            print(f"{YELLOW}!{RESET} {var} appears to be a placeholder - please update with real value")
    
    if missing_vars:
        print(f"{RED}✗{RESET} Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print(f"{GREEN}✓{RESET} All required environment variables present")
    return True


def main():
    """Run verification checks."""
    print(f"\n{YELLOW}=== Social Media Analytics AI Agent - Setup Verification ==={RESET}\n")
    
    all_checks_passed = True
    
    # Check core files
    print(f"{YELLOW}Checking Core Files...{RESET}")
    checks = [
        ("requirements.txt", "Requirements file"),
        (".env.example", "Environment example file"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "README documentation"),
        ("Makefile", "Makefile"),
    ]
    
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    # Check application structure
    print(f"\n{YELLOW}Checking Application Structure...{RESET}")
    app_checks = [
        ("app", "Application directory"),
        ("app/main.py", "Main application file"),
        ("app/core", "Core module"),
        ("app/api", "API module"),
        ("app/agents", "Agents module"),
        ("app/models", "Models module"),
        ("app/schemas", "Schemas module"),
        ("app/services", "Services module"),
        ("app/tools", "Tools module"),
        ("app/db", "Database module"),
    ]
    
    for path, description in app_checks:
        if "/" in path and not path.endswith(".py"):
            result = check_directory_exists(path, description)
        else:
            result = check_file_exists(path, description)
        if not result:
            all_checks_passed = False
    
    # Check tests
    print(f"\n{YELLOW}Checking Tests...{RESET}")
    test_checks = [
        ("tests", "Tests directory"),
        ("tests/conftest.py", "Pytest configuration"),
        ("tests/unit", "Unit tests directory"),
        ("tests/integration", "Integration tests directory"),
    ]
    
    for path, description in test_checks:
        if path.endswith(".py"):
            result = check_file_exists(path, description)
        else:
            result = check_directory_exists(path, description)
        if not result:
            all_checks_passed = False
    
    # Check scripts
    print(f"\n{YELLOW}Checking Scripts...{RESET}")
    script_checks = [
        ("scripts", "Scripts directory"),
        ("scripts/init_db.py", "Database initialization script"),
        ("scripts/create_test_user.py", "Test user creation script"),
        ("scripts/run_tests.sh", "Test runner script"),
    ]
    
    for path, description in script_checks:
        if path.endswith(".py") or path.endswith(".sh"):
            result = check_file_exists(path, description)
        else:
            result = check_directory_exists(path, description)
        if not result:
            all_checks_passed = False
    
    # Check environment
    if not check_env_file():
        all_checks_passed = False
    
    # Check Python imports
    print(f"\n{YELLOW}Checking Python Imports...{RESET}")
    try:
        import fastapi
        print(f"{GREEN}✓{RESET} FastAPI installed")
    except ImportError:
        print(f"{RED}✗{RESET} FastAPI not installed. Run: pip install -r requirements.txt")
        all_checks_passed = False
    
    try:
        import langchain
        print(f"{GREEN}✓{RESET} LangChain installed")
    except ImportError:
        print(f"{RED}✗{RESET} LangChain not installed. Run: pip install -r requirements.txt")
        all_checks_passed = False
    
    try:
        import sqlalchemy
        print(f"{GREEN}✓{RESET} SQLAlchemy installed")
    except ImportError:
        print(f"{RED}✗{RESET} SQLAlchemy not installed. Run: pip install -r requirements.txt")
        all_checks_passed = False
    
    # Summary
    print(f"\n{YELLOW}=== Verification Summary ==={RESET}")
    if all_checks_passed:
        print(f"{GREEN}✓ All checks passed! Your setup is complete.{RESET}")
        print(f"\n{YELLOW}Next Steps:{RESET}")
        print("1. Update .env with your API keys")
        print("2. Start the application:")
        print("   - Docker: docker-compose up -d")
        print("   - Local: uvicorn app.main:app --reload")
        print("3. Visit http://localhost:8000/docs")
        return 0
    else:
        print(f"{RED}✗ Some checks failed. Please fix the issues above.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
