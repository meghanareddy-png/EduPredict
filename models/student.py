"""
Student Model
"""

from datetime import datetime
from models import db

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id", ondelete="RESTRICT"), nullable=False)
    class_grade = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship("Department", backref=db.backref("students", lazy="dynamic"))
    semester = db.relationship("Semester", backref=db.backref("students", lazy="dynamic"))
    marks = db.relationship("Mark", backref="student", cascade="all, delete-orphan", lazy="dynamic")
    attendance_records = db.relationship("Attendance", backref="student", cascade="all, delete-orphan", lazy="dynamic")
    submissions = db.relationship("AssignmentSubmission", backref="student", cascade="all, delete-orphan", lazy="dynamic")
    activities = db.relationship("Activity", backref="student", cascade="all, delete-orphan", lazy="dynamic")
    predictions = db.relationship("Prediction", backref="student", cascade="all, delete-orphan", order_by="desc(Prediction.created_at)", lazy="dynamic")
    feedback = db.relationship("FacultyFeedback", backref="student", cascade="all, delete-orphan", lazy="dynamic")
    parent_links = db.relationship("ParentStudent", backref="student", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department.name if self.department else None,
            "semester": self.semester.name if self.semester else None,
            "class_grade": self.class_grade,
            "created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else None
        }
