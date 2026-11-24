"""
Faculty Model
"""

from datetime import datetime
from models import db

class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    faculty_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship("Department", backref=db.backref("faculty_members", lazy="dynamic"))
    assignments = db.relationship("FacultySubject", backref="faculty", cascade="all, delete-orphan", lazy="dynamic")
    feedback_given = db.relationship("FacultyFeedback", backref="faculty", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "faculty_id": self.faculty_id,
            "full_name": self.full_name,
            "email": self.email,
            "department": self.department.name if self.department else None,
            "created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else None
        }
