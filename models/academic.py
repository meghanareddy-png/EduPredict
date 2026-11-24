"""
Academic Structure Models
Contains: Department, Semester, Subject, FacultySubject, StudentSubject,
Attendance, Mark, Assignment, AssignmentSubmission, Activity.
"""

from datetime import datetime
from models import db

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("name", "academic_year", name="uk_sem_year"),
    )

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    credits = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department = db.relationship("Department", backref="subjects")
    semester = db.relationship("Semester", backref="subjects")

class FacultySubject(db.Model):
    __tablename__ = "faculty_subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="CASCADE"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    class_grade = db.Column(db.String(50), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")

    __table_args__ = (
        db.UniqueConstraint("faculty_id", "subject_id", "class_grade", "academic_year", name="uk_faculty_assignment"),
    )

class StudentSubject(db.Model):
    __tablename__ = "student_subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(30), default="Enrolled")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")

    __table_args__ = (
        db.UniqueConstraint("student_id", "subject_id", "semester_id", name="uk_student_enroll"),
    )

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), default="Present")  # 'Present', 'Absent', 'Excused', 'Late'
    total_sessions = db.Column(db.Integer, default=1)
    attended_sessions = db.Column(db.Integer, default=1)
    recorded_by = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")

class Mark(db.Model):
    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_type = db.Column(db.String(50), nullable=False)  # 'Internal 1', 'Internal 2', 'Midterm', 'Assignment', 'Practical', 'Final'
    marks_obtained = db.Column(db.Numeric(5, 2), nullable=False)
    max_marks = db.Column(db.Numeric(5, 2), default=100.00, nullable=False)
    exam_date = db.Column(db.Date, nullable=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="SET NULL"), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_marks = db.Column(db.Numeric(5, 2), default=100.00)
    due_date = db.Column(db.DateTime, nullable=False, index=True)
    class_grade = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")
    faculty = db.relationship("Faculty")
    submissions = db.relationship("AssignmentSubmission", backref="assignment", cascade="all, delete-orphan", lazy="dynamic")

class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    submission_text = db.Column(db.Text, nullable=True)
    marks_obtained = db.Column(db.Numeric(5, 2), nullable=True)
    is_completed = db.Column(db.Boolean, default=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("assignment_id", "student_id", name="uk_submission"),
    )

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'Technical Event', 'Workshop', 'Sports', 'Cultural', 'Certification', 'Achievement'
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    achievement_level = db.Column(db.String(50), default="Participation")
    event_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
