"""
EduPredict - Automated MySQL Database Setup & Migration Script
Usage:
    python database/setup_mysql.py [password]
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pymysql

def setup_mysql(password="root", host="localhost", port=3306, user="root", db_name="edupredict_db"):
    print("=" * 65)
    print(" 🚀 EduPredict MySQL Database Setup & Migration")
    print("=" * 65)
    print(f"[*] Target Host     : {host}:{port}")
    print(f"[*] MySQL User      : {user}")
    print(f"[*] Target Database : {db_name}")

    # 1. Connect to MySQL server root
    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            charset="utf8mb4",
            autocommit=True
        )
        print("[+] Connected to MySQL Server successfully! ✅")
    except Exception as e:
        print(f"\n[-] Could not connect to MySQL Server at {host}:{port} with user '{user}'.")
        print(f"    Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure your MySQL service is started (e.g. open Command Prompt as Administrator and run: net start MySQL80)")
        print("  2. Verify your root password. Run: python database/setup_mysql.py YOUR_PASSWORD")
        return False

    # 2. Create Database
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"[+] Database `{db_name}` created or already exists. ✅")
            cursor.execute(f"USE `{db_name}`;")
    except Exception as e:
        print(f"[-] Failed to create database `{db_name}`: {e}")
        conn.close()
        return False

    # 3. Create or update .env file
    env_content = f"""# EduPredict Environment Configuration (MySQL Active)
MYSQL_HOST={host}
MYSQL_PORT={port}
MYSQL_USER={user}
MYSQL_PASSWORD={password}
MYSQL_DB={db_name}
USE_MYSQL=true

SECRET_KEY=edupredict_super_secret_session_key_2026
PORT=5000
DEBUG=True
"""
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"[+] Configured `{os.path.basename(env_path)}` with MySQL credentials. ✅")

    conn.close()

    # 4. Initialize tables and seed through SQLAlchemy
    print("\n[*] Initializing tables and seeding initial demo data...")
    from app import create_app
    from models import db
    from database.seed import seed_database

    app = create_app()
    with app.app_context():
        db.create_all()
        seed_database(app)

    print("\n[+] MySQL Setup Complete! All tables and accounts are ready! 🎉")
    print("=" * 65)
    return True

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 else ""
    # Try common default passwords if not supplied: empty string, 'root', 'admin', 'password'
    passwords_to_try = [pwd] if pwd else ["", "root", "admin", "password", "123456", "12345678", "MySQL80"]
    
    success = False
    for p in passwords_to_try:
        print(f"[*] Trying password: '{p}' ...")
        if setup_mysql(password=p):
            success = True
            break
            
    if not success and not pwd:
        print("\n👉 Please run with your MySQL root password:")
        print("   python database/setup_mysql.py YOUR_MYSQL_PASSWORD")
