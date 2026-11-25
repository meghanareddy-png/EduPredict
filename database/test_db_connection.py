"""
EduPredict Database Connection Diagnostic Utility
Run this script to test database connectivity:
    python database/test_db_connection.py
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config, get_database_uri
from app import create_app
from models import db, User, Student, Department, Mark

def test_connection():
    print("=" * 60)
    print(" 🔍 EduPredict Database Connection Diagnostics")
    print("=" * 60)
    
    uri = get_database_uri()
    engine_name = "MySQL" if "mysql" in uri else "SQLite"
    print(f"[*] Configured Engine : {engine_name}")
    print(f"[*] Connection URI    : {uri.split('@')[-1] if '@' in uri else uri}")

    app = create_app()
    with app.app_context():
        try:
            user_count = User.query.count()
            student_count = Student.query.count()
            dept_count = Department.query.count()
            marks_count = Mark.query.count()

            print("\n[+] Database connection SUCCESSFUL! ✅")
            print(f"    - Total Registered Users : {user_count}")
            print(f"    - Total Student Profiles : {student_count}")
            print(f"    - Academic Departments   : {dept_count}")
            print(f"    - Examination Marks Logs : {marks_count}")
            print("\n[+] Demo Accounts Ready:")
            for u in User.query.limit(4).all():
                print(f"    • Role: {u.role.upper():<8} | Username: {u.username:<16} | Name: {u.full_name}")
            print("=" * 60)
        except Exception as e:
            print(f"\n[-] Database connection FAILED ❌")
            print(f"    Error: {e}")
            print("=" * 60)

if __name__ == "__main__":
    test_connection()
