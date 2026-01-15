"""
Verification script to check if the project is set up correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_imports():
    """Check if all required packages are installed"""
    print("🔍 Checking Python packages...")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("langchain", "LangChain"),
        ("asyncpg", "AsyncPG"),
    ]
    
    missing = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - MISSING")
            missing.append(package)
    
    return missing


def check_env_file():
    """Check if .env file exists"""
    print("\n🔍 Checking environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("  ✓ .env file found")
        return True
    else:
        print("  ✗ .env file not found")
        print("    → Copy env.example to .env and configure it")
        return False


def check_env_variables():
    """Check if required environment variables are set"""
    try:
        from app.core.config import get_settings
        
        settings = get_settings()
        
        checks = [
            ("DATABASE_URL", settings.DATABASE_URL),
            ("OPENROUTER_API_KEY", settings.OPENROUTER_API_KEY),
            ("OPENROUTER_MODEL", settings.OPENROUTER_MODEL),
        ]
        
        all_set = True
        for name, value in checks:
            if value and not value.startswith("your_") and not value.startswith("postgresql://user:password"):
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} - NOT CONFIGURED")
                all_set = False
        
        return all_set
    except Exception as e:
        print(f"  ✗ Error loading settings: {e}")
        return False


def check_project_structure():
    """Check if all required directories exist"""
    print("\n🔍 Checking project structure...")
    
    required_dirs = [
        "app",
        "app/api",
        "app/agents",
        "app/tools",
        "app/services",
        "app/repositories",
        "app/domain",
        "app/db",
        "app/core",
        "app/tests",
        "scripts",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Todo AI Agent - Setup Verification")
    print("=" * 60)
    
    # Check imports
    missing_packages = check_imports()
    
    # Check .env file
    env_exists = check_env_file()
    
    # Check environment variables
    if env_exists:
        env_configured = check_env_variables()
    else:
        env_configured = False
    
    # Check project structure
    structure_ok = check_project_structure()
    
    # Final verdict
    print("\n" + "=" * 60)
    if not missing_packages and env_configured and structure_ok:
        print("✅ Setup verification PASSED!")
        print("\nYou're ready to run the application:")
        print("  → uvicorn app.main:app --reload")
        print("  → or: make dev")
        return 0
    else:
        print("❌ Setup verification FAILED!")
        print("\nPlease fix the issues above:")
        
        if missing_packages:
            print(f"\n1. Install missing packages:")
            print(f"   → pip install -r requirements.txt")
        
        if not env_exists or not env_configured:
            print(f"\n2. Configure environment:")
            print(f"   → Copy ENV_TEMPLATE.txt to .env")
            print(f"   → Edit .env with your credentials")
        
        if not structure_ok:
            print(f"\n3. Verify project structure")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())

