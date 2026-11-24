"""
Parent Dashboard Routes & APIs
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_file
from models import (
    db, Parent, ParentStudent, Student, Mark, Attendance, Assignment,
    AssignmentSubmission, FacultyFeedback, Notification, Prediction
)
from routes.helpers import login_required, role_required, get_current_user
from routes.student import _compute_student_analytics

parent_bp = Blueprint("parent", __name__, url_prefix="/parent")

@parent_bp.route("/dashboard")
@login_required
@role_required("parent")
def dashboard():
    user = get_current_user()
    parent = Parent.query.filter_by(user_id=user.id).first()
    if not parent:
        flash("Parent profile not found.", "danger")
        return redirect(url_for("auth.login"))

    # Linked children
    linked_records = ParentStudent.query.filter_by(parent_id=parent.id, is_verified=True).all()
    if not linked_records:
        flash("No verified student is linked to your parent account. Please contact school administration.", "warning")
        return render_template("parent_dashboard.html", parent=parent, children=[], active_child=None)

    children = [lr.student for lr in linked_records]

    # Selected child
    child_id = request.args.get("child_id")
    active_child = None
    if child_id:
        active_child = next((c for c in children if str(c.id) == str(child_id)), None)
    if not active_child:
        active_child = children[0]

    analytics = _compute_student_analytics(active_child)

    marks_list = Mark.query.filter_by(student_id=active_child.id).order_by(Mark.exam_date.desc()).all()
    feedback_list = FacultyFeedback.query.filter_by(student_id=active_child.id).order_by(FacultyFeedback.created_at.desc()).all()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(8).all()

    # Subject performance chart
    subject_marks_dict = {}
    for m in marks_list:
        sub_name = m.subject.name if m.subject else "General"
        pct = (float(m.marks_obtained) / float(m.max_marks)) * 100
        if sub_name not in subject_marks_dict:
            subject_marks_dict[sub_name] = []
        subject_marks_dict[sub_name].append(pct)

    chart_subjects = list(subject_marks_dict.keys())
    chart_subject_scores = [round(sum(scores)/len(scores), 1) for scores in subject_marks_dict.values()]

    return render_template(
        "parent_dashboard.html",
        parent=parent,
        children=children,
        active_child=active_child,
        analytics=analytics,
        marks_list=marks_list,
        feedback_list=feedback_list,
        notifications=notifications,
        chart_subjects=chart_subjects,
        chart_subject_scores=chart_subject_scores
    )

@parent_bp.route("/download-report/<int:student_id>")
@login_required
@role_required("parent")
def download_report(student_id):
    user = get_current_user()
    parent = Parent.query.filter_by(user_id=user.id).first()
    
    # Verify relationship
    link = ParentStudent.query.filter_by(parent_id=parent.id, student_id=student_id, is_verified=True).first()
    if not link:
        flash("Unauthorized to access reports for this student.", "danger")
        return redirect(url_for("parent.dashboard"))

    student = Student.query.get_or_404(student_id)
    analytics = _compute_student_analytics(student)
    marks_list = Mark.query.filter_by(student_id=student.id).all()
    feedback_list = FacultyFeedback.query.filter_by(student_id=student.id).all()

    from routes.report_generator import generate_student_pdf_report
    pdf_buffer = generate_student_pdf_report(student, analytics, marks_list, feedback_list, parent_name=parent.full_name)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"EduPredict_Progress_Report_{student.student_id}.pdf",
        mimetype="application/pdf"
    )
