"""
Prediction, Feedback, and Notification Models
"""

from datetime import datetime
from models import db

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    predicted_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    performance_category = db.Column(db.String(50), nullable=False)  # 'Distinction', 'First Class', 'Second Class', 'Remedial'
    risk_level = db.Column(db.String(20), nullable=False, index=True)  # 'Low', 'Medium', 'High'
    model_version = db.Column(db.String(50), default="v1.0-rf-regressor")
    weak_areas = db.Column(db.Text, nullable=True)  # JSON or comma-separated subjects
    recommendations = db.Column(db.Text, nullable=True)  # JSON or pipe-separated advice
    input_features = db.Column(db.Text, nullable=True)  # JSON string of input features
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FacultyFeedback(db.Model):
    __tablename__ = "faculty_feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id", ondelete="CASCADE"), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="Academic Progress")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default="General")  # 'Attendance', 'Marks', 'Assignment', 'Exam', 'Feedback'
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.notification_type,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%b %d, %H:%M") if self.created_at else None
        }
