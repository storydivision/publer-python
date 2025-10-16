#!/usr/bin/env python3
"""
Verify that the Publer API client is set up correctly.

Run this script to check:
- Package installation
- Environment configuration
- API connectivity
"""

import sys
from pathlib import Path


def check_imports() -> bool:
    """Check that all required packages can be imported."""
    print("Checking imports...")
    try:
        import httpx
        import pydantic
        import dotenv
        from publer import PublerClient, AsyncPublerClient
        from publer.exceptions import PublerAPIError
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("  Run: pip install -e .")
        return False


def check_env_file() -> bool:
    """Check that .env file exists."""
    print("\nChecking environment configuration...")
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_example.exists():
        print("✗ .env.example not found")
        return False

    if not env_file.exists():
        print("✗ .env file not found")
        print("  Run: cp .env.example .env")
        print("  Then edit .env and add your API key")
        return False

    print("✓ .env file exists")
    return True


def check_api_key() -> bool:
    """Check that API key is configured."""
    print("\nChecking API key...")
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("PUBLER_API_KEY")

    if not api_key:
        print("✗ PUBLER_API_KEY not set in .env file")
        print("  Edit .env and add: PUBLER_API_KEY=your_key_here")
        return False

    if api_key == "your_api_key_here":
        print("✗ PUBLER_API_KEY still has default value")
        print("  Edit .env and add your actual API key")
        return False

    print(f"✓ API key configured (starts with: {api_key[:10]}...)")
    return True


def check_api_connection() -> bool:
    """Check that we can connect to the API."""
    print("\nTesting API connection...")
    try:
        from publer import PublerClient
        from publer.exceptions import AuthenticationError

        with PublerClient() as client:
            # Test by fetching workspaces (simplest endpoint)
            workspaces = client.workspaces.list()
            print(f"✓ Connected successfully!")
            print(f"  Found {len(workspaces)} workspace(s)")
            if workspaces:
                print(f"  First workspace: {workspaces[0].name}")
            return True

    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        return False
    except AuthenticationError:
        print("✗ Authentication failed")
        print("  Check that your API key is correct")
        print("  Ensure you have a Business or Enterprise plan")
        return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def check_project_structure() -> bool:
    """Check that project structure is correct."""
    print("\nChecking project structure...")
    required_paths = [
        "publer/__init__.py",
        "publer/client.py",
        "publer/session.py",
        "publer/exceptions.py",
        "publer/resources/base.py",
        "tests/conftest.py",
        "pyproject.toml",
        ".gitignore",
    ]

    all_exist = True
    for path_str in required_paths:
        path = Path(path_str)
        if not path.exists():
            print(f"✗ Missing: {path_str}")
            all_exist = False

    if all_exist:
        print("✓ Project structure is correct")
    return all_exist


def main() -> int:
    """Run all verification checks."""
    print("=" * 60)
    print("Publer API Client - Setup Verification")
    print("=" * 60)

    checks = [
        ("Project Structure", check_project_structure),
        ("Package Imports", check_imports),
        ("Environment File", check_env_file),
        ("API Key", check_api_key),
        ("API Connection", check_api_connection),
    ]

    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"\n✗ {name} check failed with error: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for (name, _), result in zip(checks, results):
        status = "✓" if result else "✗"
        print(f"{status} {name}")

    print(f"\nPassed: {passed}/{total}")

    if all(results):
        print("\n🎉 All checks passed! You're ready to start developing.")
        print("\nNext steps:")
        print("  1. Read QUICKSTART.md for usage examples")
        print("  2. Check examples/ directory for code samples")
        print("  3. See CONTRIBUTING.md to add new features")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
