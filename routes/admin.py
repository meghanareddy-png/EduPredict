"""
Administrator Console Routes & Management
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from models import (
    db, User, Student, Parent, Faculty, Department, Semester, Subject,
    FacultySubject, ParentStudent, Prediction, Notification
)
from routes.helpers import login_required, role_required
from ml.train_model import train_and_save_models
from ml.predict import get_model_metadata

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    # Counts
    total_users = User.query.count()
    total_students = Student.query.count()
    total_faculty = Faculty.query.count()
    total_parents = Parent.query.count()
    total_departments = Department.query.count()
    total_subjects = Subject.query.count()

    # Lists
    users = User.query.order_by(User.created_at.desc()).all()
    departments = Department.query.all()
    semesters = Semester.query.all()
    subjects = Subject.query.all()
    faculty_list = Faculty.query.all()
    student_list = Student.query.all()
    parent_list = Parent.query.all()
    faculty_assignments = FacultySubject.query.all()
    parent_links = ParentStudent.query.all()

    # ML Metadata
    ml_meta = get_model_metadata()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_students=total_students,
        total_faculty=total_faculty,
        total_parents=total_parents,
        total_departments=total_departments,
        total_subjects=total_subjects,
        users=users,
        departments=departments,
        semesters=semesters,
        subjects=subjects,
        faculty_list=faculty_list,
        student_list=student_list,
        parent_list=parent_list,
        faculty_assignments=faculty_assignments,
        parent_links=parent_links,
        ml_meta=ml_meta
    )

@admin_bp.route("/toggle-user/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == "admin":
        flash("Root administrator cannot be deactivated.", "danger")
        return redirect(url_for("admin.dashboard"))
    user.is_active = not user.is_active
    db.session.commit()
    status_str = "activated" if user.is_active else "deactivated"
    flash(f"User account '{user.username}' has been {status_str}.", "info")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/add-department", methods=["POST"])
@login_required
@role_required("admin")
def add_department():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    if code and name:
        if Department.query.filter_by(code=code).first():
            flash(f"Department code '{code}' already exists.", "danger")
        else:
            db.session.add(Department(code=code, name=name))
            db.session.commit()
            flash(f"Department '{name}' added successfully.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/add-subject", methods=["POST"])
@login_required
@role_required("admin")
def add_subject():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    dept_id = request.form.get("department_id")
    sem_id = request.form.get("semester_id")
    credits = int(request.form.get("credits", 3))

    if code and name and dept_id and sem_id:
        if Subject.query.filter_by(code=code).first():
            flash(f"Subject code '{code}' already exists.", "danger")
        else:
            db.session.add(Subject(code=code, name=name, department_id=int(dept_id), semester_id=int(sem_id), credits=credits))
            db.session.commit()
            flash(f"Subject '{name}' added successfully.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/assign-faculty", methods=["POST"])
@login_required
@role_required("admin")
def assign_faculty():
    faculty_id = request.form.get("faculty_id")
    subject_id = request.form.get("subject_id")
    class_grade = request.form.get("class_grade", "").strip()
    academic_year = request.form.get("academic_year", "2026-2027").strip()

    if faculty_id and subject_id and class_grade:
        existing = FacultySubject.query.filter_by(
            faculty_id=int(faculty_id),
            subject_id=int(subject_id),
            class_grade=class_grade,
            academic_year=academic_year
        ).first()
        if not existing:
            db.session.add(FacultySubject(
                faculty_id=int(faculty_id),
                subject_id=int(subject_id),
                class_grade=class_grade,
                academic_year=academic_year
            ))
            db.session.commit()
            flash("Faculty assignment established successfully.", "success")
        else:
            flash("This assignment already exists.", "warning")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/link-parent", methods=["POST"])
@login_required
@role_required("admin")
def link_parent():
    parent_id = request.form.get("parent_id")
    student_id = request.form.get("student_id")
    relationship = request.form.get("relationship", "Parent/Guardian")

    if parent_id and student_id:
        link = ParentStudent.query.filter_by(parent_id=int(parent_id), student_id=int(student_id)).first()
        if not link:
            db.session.add(ParentStudent(
                parent_id=int(parent_id),
                student_id=int(student_id),
                relationship_type=relationship,
                is_verified=True
            ))
            db.session.commit()
            flash("Parent-Student verified link established.", "success")
        else:
            flash("Parent and Student are already linked.", "info")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/retrain-model", methods=["POST"])
@login_required
@role_required("admin")
def retrain_model():
    """Triggers ML model re-training."""
    try:
        meta = train_and_save_models()
        flash(f"ML models re-trained successfully! R² score: {meta['metrics']['regression']['r2_score']}", "success")
    except Exception as e:
        flash(f"Re-training failed: {str(e)}", "danger")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/broadcast-announcement", methods=["POST"])
@login_required
@role_required("admin")
def broadcast_announcement():
    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()
    target_role = request.form.get("target_role", "all")

    if title and message:
        if target_role == "all":
            users = User.query.all()
        else:
            users = User.query.filter_by(role=target_role).all()

        for u in users:
            db.session.add(Notification(
                user_id=u.id,
                title=title,
                message=message,
                notification_type="Announcement"
            ))
        db.session.commit()
        flash(f"Announcement sent to {len(users)} users.", "success")
    return redirect(url_for("admin.dashboard"))
