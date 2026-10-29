#!/usr/bin/env python3
"""
Library Management System - Pre-Launch Verification Script
Checks if all components are properly set up before running the application
"""

import sys
import os
import subprocess
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass  # reported by the package check below

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def check_mark(text):
    print(f"{GREEN}✅ {text}{RESET}")

def cross_mark(text):
    print(f"{RED}❌ {text}{RESET}")

def warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def info(text):
    print(f"ℹ️  {text}")

def check_file_exists(path, name):
    """Check if a file/directory exists"""
    if Path(path).exists():
        check_mark(f"{name} exists")
        return True
    else:
        cross_mark(f"{name} NOT FOUND: {path}")
        return False

def check_python_package(package_name, module_name=None):
    """Check if a Python package is installed"""
    mod = module_name or package_name
    try:
        __import__(mod)
        check_mark(f"Package '{package_name}' is installed")
        return True
    except ImportError:
        cross_mark(f"Package '{package_name}' NOT INSTALLED")
        warning(f"Run: pip install {package_name}")
        return False

def get_db_params():
    """Read MySQL connection parameters from the environment / .env"""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "project"),
    }

def check_mysql_connection():
    """Check if MySQL is running and accessible"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(**get_db_params())
        check_mark("MySQL connection successful")
        conn.close()
        return True
    except Exception as e:
        cross_mark(f"MySQL connection failed: {str(e)}")
        return False

def check_database_tables():
    """Check if database tables exist"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(**get_db_params())
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        required_tables = ['book', 'member', 'member_details', 'issue_and_return']
        
        missing = []
        for table in required_tables:
            if table in table_names:
                check_mark(f"Table '{table}' exists")
            else:
                missing.append(table)
                cross_mark(f"Table '{table}' NOT FOUND")
        
        cursor.close()
        conn.close()
        
        return len(missing) == 0
    except Exception as e:
        cross_mark(f"Failed to check tables: {str(e)}")
        return False

def main():
    print_header("📚 Library Management System - Pre-Launch Verification")
    
    all_checks_passed = True
    
    # Check directory structure
    print(f"{YELLOW}Checking Directory Structure...{RESET}")
    all_checks_passed &= check_file_exists("backend/src", "backend/src/ directory")
    all_checks_passed &= check_file_exists("backend/sql", "backend/sql/ directory")
    all_checks_passed &= check_file_exists("frontend", "frontend/ directory")
    all_checks_passed &= check_file_exists("frontend/pages", "frontend/pages/ directory")
    all_checks_passed &= check_file_exists("frontend/utils", "frontend/utils/ directory")
    all_checks_passed &= check_file_exists("docs", "docs/ directory")
    
    # Check required files
    print(f"\n{YELLOW}Checking Required Files...{RESET}")
    all_checks_passed &= check_file_exists("frontend/app.py", "frontend/app.py (main router)")
    all_checks_passed &= check_file_exists("requirements.txt", "requirements.txt")
    all_checks_passed &= check_file_exists("README.md", "README.md")
    all_checks_passed &= check_file_exists("backend/sql/schema.sql", "backend/sql/schema.sql")
    all_checks_passed &= check_file_exists(".env.example", ".env.example")
    if Path(".env").exists():
        check_mark(".env exists")
    else:
        warning(".env not found - copy .env.example to .env and fill in your MySQL credentials")
    
    # Check backend modules
    print(f"\n{YELLOW}Checking Backend Modules...{RESET}")
    modules = ['main.py', 'database.py', 'books.py', 'members.py', 'issue_return.py', 'stats.py', 'backend_utils.py']
    for module in modules:
        all_checks_passed &= check_file_exists(f"backend/src/{module}", f"backend/src/{module}")
    
    # Check frontend pages and utilities
    print(f"\n{YELLOW}Checking Frontend Modules...{RESET}")
    all_checks_passed &= check_file_exists("frontend/utils/config.py", "frontend/utils/config.py")
    all_checks_passed &= check_file_exists("frontend/utils/database_helpers.py", "frontend/utils/database_helpers.py")
    pages = ['dashboard.py', 'books.py', 'members.py', 'transactions.py', 'statistics.py']
    for page in pages:
        all_checks_passed &= check_file_exists(f"frontend/pages/{page}", f"frontend/pages/{page}")
    
    # Check documentation
    print(f"\n{YELLOW}Checking Documentation...{RESET}")
    all_checks_passed &= check_file_exists("docs/FRONTEND.md", "docs/FRONTEND.md")
    all_checks_passed &= check_file_exists("docs/BACKEND.md", "docs/BACKEND.md")
    all_checks_passed &= check_file_exists("docs/INDEX.md", "docs/INDEX.md (documentation index)")
    
    # Check Python packages
    print(f"\n{YELLOW}Checking Python Packages...{RESET}")
    all_checks_passed &= check_python_package("streamlit")
    all_checks_passed &= check_python_package("pandas")
    all_checks_passed &= check_python_package("plotly")
    all_checks_passed &= check_python_package("mysql-connector-python", "mysql.connector")
    all_checks_passed &= check_python_package("python-dotenv", "dotenv")
    
    # Check Python version
    print(f"\n{YELLOW}Checking Python Version...{RESET}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        check_mark(f"Python {version.major}.{version.minor} (required: 3.7+)")
    else:
        cross_mark(f"Python {version.major}.{version.minor} (required: 3.7+)")
        all_checks_passed = False
    
    # Check imports
    print(f"\n{YELLOW}Checking Backend Imports...{RESET}")
    try:
        # Properly set up Python path for backend
        backend_src_path = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        if backend_src_path not in sys.path:
            sys.path.insert(0, backend_src_path)
        
        # Now try importing backend modules
        from database import Database
        from books import Book, BookManager
        from members import Member, MemberManager
        from issue_return import BookTransaction
        import stats
        check_mark("All backend modules can be imported")
    except ImportError as e:
        cross_mark(f"Import error: {str(e)}")
        info(f"Error details: {e}")
        all_checks_passed = False
    
    # Check frontend imports (optional - streamlit handles them)
    print(f"\n{YELLOW}Checking Frontend Configuration...{RESET}")
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
        if frontend_path not in sys.path:
            sys.path.insert(0, frontend_path)
        # Just verify config files exist, don't import (streamlit manages this)
        if Path("frontend/utils/config.py").exists() and Path("frontend/utils/database_helpers.py").exists():
            check_mark("Frontend configuration files are properly organized")
        else:
            raise FileNotFoundError("Missing frontend config files")
    except Exception as e:
        cross_mark(f"Frontend setup error: {str(e)}")
        all_checks_passed = False
    
    # Summary
    print_header("🎯 Verification Summary")
    
    if all_checks_passed:
        check_mark("All checks PASSED! ✨")
        info("Your system is ready to run the dashboard.")
        info("Command: streamlit run frontend/app.py")
        info("Documentation: See docs/INDEX.md for guides (FRONTEND.md, BACKEND.md)")
        return 0
    else:
        cross_mark("Some checks FAILED")
        warning("Please fix the issues above before running the dashboard.")
        info("Documentation: See docs/INDEX.md for troubleshooting and setup help.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Verification cancelled by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {str(e)}{RESET}")
        sys.exit(1)
