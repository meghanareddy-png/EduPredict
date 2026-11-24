"""
EduPredict Models Package
Exports SQLAlchemy database instance and all entity models.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.academic import Department, Semester, Subject, FacultySubject, StudentSubject, Attendance, Mark, Assignment, AssignmentSubmission, Activity
from models.student import Student
from models.parent import Parent, ParentStudent
from models.faculty import Faculty
from models.prediction import Prediction, FacultyFeedback, Notification

__all__ = [
    "db",
    "User",
    "Department",
    "Semester",
    "Subject",
    "FacultySubject",
    "StudentSubject",
    "Attendance",
    "Mark",
    "Assignment",
    "AssignmentSubmission",
    "Activity",
    "Student",
    "Parent",
    "ParentStudent",
    "Faculty",
    "Prediction",
    "FacultyFeedback",
    "Notification"
]
