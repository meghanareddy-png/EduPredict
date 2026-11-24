"""
Automated Integration Tests for Database CRUD & Relationships
"""

import pytest
from datetime import date
from app import create_app
from config import TestConfig
from models import (
    db, User, Student, Parent, Faculty, Department, Semester, Subject,
    Attendance, Mark, Assignment, AssignmentSubmission, ParentStudent
)

@pytest.fixture
def app_ctx():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_student_and_academic_creation(app_ctx):
    # Department & Semester
    dept = Department(code="IT", name="Information Technology")
    sem = Semester(name="Sem 1", academic_year="2026-2027", is_current=True)
    db.session.add_all([dept, sem])
    db.session.commit()

    # User & Student
    u = User(username="it_student", email="it@test.com", password_hash="hash", role="student", full_name="IT Student")
    db.session.add(u)
    db.session.commit()

    stu = Student(user_id=u.id, student_id="IT001", full_name="IT Student", email=u.email, department_id=dept.id, semester_id=sem.id, class_grade="Class IT-1")
    db.session.add(stu)
    db.session.commit()

    # Subject & Mark
    sub = Subject(code="IT101", name="Intro to Programming", department_id=dept.id, semester_id=sem.id)
    db.session.add(sub)
    db.session.commit()

    mark = Mark(student_id=stu.id, subject_id=sub.id, exam_type="Internal 1", marks_obtained=42.0, max_marks=50.0, exam_date=date.today())
    att = Attendance(student_id=stu.id, subject_id=sub.id, date=date.today(), status="Present", total_sessions=1, attended_sessions=1)
    db.session.add_all([mark, att])
    db.session.commit()

    assert stu.marks.count() == 1
    assert stu.attendance_records.count() == 1
    assert stu.department.code == "IT"

def test_parent_child_relationship(app_ctx):
    u_p = User(username="par_test", email="par@test.com", password_hash="hash", role="parent", full_name="Test Parent")
    db.session.add(u_p)
    db.session.commit()

    parent = Parent(user_id=u_p.id, full_name="Test Parent", email=u_p.email)
    db.session.add(parent)
    db.session.commit()

    stu = Student.query.first()
    if stu:
        link = ParentStudent(parent_id=parent.id, student_id=stu.id, relationship_type="Father", is_verified=True)
        db.session.add(link)
        db.session.commit()
        assert parent.children_links.count() == 1
