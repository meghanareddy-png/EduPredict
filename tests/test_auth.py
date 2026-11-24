"""
Automated Unit Tests for User Authentication and Role Permissions
"""

import pytest
from app import create_app
from config import TestConfig
from models import db, User, Student

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_user_password_hashing(client):
    user = User(username="tester", email="test@test.com", role="student", full_name="Test User")
    user.set_password("MySecurePass123!")
    assert user.password_hash != "MySecurePass123!"
    assert user.check_password("MySecurePass123!") is True
    assert user.check_password("WrongPassword") is False

def test_login_flow(client):
    user = User(username="student1", email="student1@test.com", role="student", full_name="Student One")
    user.set_password("StudentPass123!")
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        student_id="STU-TEST-001",
        full_name="Student One",
        email="student1@test.com",
        department_id=1,
        semester_id=1,
        class_grade="CSE-1A"
    )
    db.session.add(student)
    db.session.commit()

    # Valid Login
    res = client.post("/login", data={
        "login_id": "student1",
        "password": "StudentPass123!"
    }, follow_redirects=True)
    assert res.status_code == 200

    # Logout to clear session
    client.get("/logout", follow_redirects=True)

    # Invalid Login
    res_bad = client.post("/login", data={
        "login_id": "student1",
        "password": "BadPassword!"
    }, follow_redirects=True)
    assert b"Invalid credentials" in res_bad.data

def test_demo_logins(client):
    for role in ["student", "faculty", "parent", "admin"]:
        res = client.get(f"/demo-login/{role}", follow_redirects=True)
        assert res.status_code == 200

def test_logout(client):
    res = client.get("/logout", follow_redirects=True)
    assert res.status_code == 200
    assert b"signed out safely" in res.data
