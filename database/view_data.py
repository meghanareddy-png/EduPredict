"""
EduPredict - Stored Data Viewer Utility
Run this script to inspect all database records in the terminal:
    python database/view_data.py
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from models import (
    db, User, Student, Parent, Faculty, Department, Semester,
    Subject, Attendance, Mark, Assignment, Prediction, FacultyFeedback
)

def view_stored_data():
    app = create_app()
    with app.app_context():
        print("=" * 75)
        print(" 📂 EDUPREDICT STORED DATABASE RECORDS (edupredict.db)")
        print("=" * 75)

        # 1. USERS
        print("\n👥 1. REGISTERED USERS TABLE ('users')")
        print("-" * 75)
        print(f"{'ID':<4} | {'ROLE':<8} | {'USERNAME':<16} | {'FULL NAME':<22} | {'EMAIL'}")
        print("-" * 75)
        for u in User.query.all():
            print(f"{u.id:<4} | {u.role.upper():<8} | {u.username:<16} | {u.full_name:<22} | {u.email}")

        # 2. STUDENTS
        print("\n🎓 2. STUDENT PROFILES TABLE ('students')")
        print("-" * 75)
        print(f"{'ID':<4} | {'STUDENT ID':<12} | {'FULL NAME':<20} | {'CLASS':<12} | {'DEPARTMENT'}")
        print("-" * 75)
        for s in Student.query.all():
            dept_name = s.department.name if s.department else "General"
            print(f"{s.id:<4} | {s.student_id:<12} | {s.full_name:<20} | {s.class_grade:<12} | {dept_name}")

        # 3. MARKS
        print("\n📝 3. EXAMINATION MARKS LOGS ('marks')")
        print("-" * 75)
        print(f"{'ID':<4} | {'STUDENT':<16} | {'SUBJECT':<24} | {'EXAM TYPE':<16} | {'SCORE'}")
        print("-" * 75)
        for m in Mark.query.limit(10).all():
            stu_name = m.student.full_name if m.student else f"Student #{m.student_id}"
            sub_name = m.subject.name if m.subject else "Course"
            pct = round((float(m.marks_obtained) / float(m.max_marks)) * 100, 1)
            print(f"{m.id:<4} | {stu_name:<16} | {sub_name:<24} | {m.exam_type:<16} | {m.marks_obtained}/{m.max_marks} ({pct}%)")
        if Mark.query.count() > 10:
            print(f"... and {Mark.query.count() - 10} more marks records.")

        # 4. ATTENDANCE
        print("\n📅 4. ATTENDANCE SESSIONS TABLE ('attendance')")
        print("-" * 75)
        print(f"{'ID':<4} | {'STUDENT':<16} | {'SUBJECT':<24} | {'ATTENDED':<10} | {'TOTAL':<8} | {'PERCENTAGE'}")
        print("-" * 75)
        for a in Attendance.query.all():
            stu_name = a.student.full_name if a.student else f"Student #{a.student_id}"
            sub_name = a.subject.name if a.subject else "Course"
            pct = round((a.attended_sessions / a.total_sessions) * 100, 1) if a.total_sessions > 0 else 0
            print(f"{a.id:<4} | {stu_name:<16} | {sub_name:<24} | {a.attended_sessions:<10} | {a.total_sessions:<8} | {pct}%")

        # 5. PREDICTIONS
        print("\n🔮 5. MACHINE LEARNING PREDICTIONS ('predictions')")
        print("-" * 75)
        print(f"{'ID':<4} | {'STUDENT':<16} | {'PREDICTED %':<12} | {'CATEGORY':<14} | {'RISK LEVEL'}")
        print("-" * 75)
        for p in Prediction.query.all():
            stu_name = p.student.full_name if p.student else f"Student #{p.student_id}"
            print(f"{p.id:<4} | {stu_name:<16} | {p.predicted_percentage}%{'':<6} | {p.performance_category:<14} | {p.risk_level}")

        print("\n" + "=" * 75)
        print(f"📍 Database File Location: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'edupredict.db'))}")
        print("=" * 75)

if __name__ == "__main__":
    view_stored_data()
