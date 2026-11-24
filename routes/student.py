"""
Student Dashboard Routes & APIs
"""

from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, send_file
from models import (
    db, Student, StudentSubject, Subject, Attendance, Mark, Assignment,
    AssignmentSubmission, Activity, Prediction, FacultyFeedback, Notification
)
from routes.helpers import login_required, role_required, get_current_user
from ml.predict import predict_student_performance, simulate_future_score

student_bp = Blueprint("student", __name__, url_prefix="/student")

def _compute_student_analytics(student):
    """Computes real-time KPI metrics and feature vector for predictions."""
    # 1. Total Enrolled Subjects
    enrolled_subs = StudentSubject.query.filter_by(student_id=student.id).all()
    total_subjects = len(enrolled_subs)

    # 2. Attendance %
    att_records = Attendance.query.filter_by(student_id=student.id).all()
    total_sessions = sum(a.total_sessions for a in att_records) if att_records else 0
    attended_sessions = sum(a.attended_sessions for a in att_records) if att_records else 0
    attendance_pct = round((attended_sessions / total_sessions) * 100, 1) if total_sessions > 0 else 75.0
    missed_sessions = total_sessions - attended_sessions

    # 3. Average Internal Marks
    marks_records = Mark.query.filter_by(student_id=student.id).all()
    if marks_records:
        total_obt = sum(float(m.marks_obtained) for m in marks_records)
        total_max = sum(float(m.max_marks) for m in marks_records)
        avg_internal_pct = round((total_obt / total_max) * 100, 1) if total_max > 0 else 65.0
    else:
        avg_internal_pct = 65.0

    # 4. Assignment Completion
    # Find assignments targeted to student's class
    class_assignments = Assignment.query.filter_by(class_grade=student.class_grade).all()
    total_assignments = len(class_assignments)
    submissions = AssignmentSubmission.query.filter_by(student_id=student.id, is_completed=True).all()
    completed_assignments = len(submissions)
    pending_assignments = max(0, total_assignments - completed_assignments)
    assignment_pct = round((completed_assignments / total_assignments) * 100, 1) if total_assignments > 0 else 70.0

    # 5. Practical Marks average
    prac_marks = [float(m.marks_obtained) / float(m.max_marks) * 100 for m in marks_records if "practical" in m.exam_type.lower()]
    practical_pct = round(sum(prac_marks) / len(prac_marks), 1) if prac_marks else avg_internal_pct

    # 6. Latest Prediction
    latest_pred = Prediction.query.filter_by(student_id=student.id).order_by(Prediction.created_at.desc()).first()
    if not latest_pred:
        # Run live ML prediction
        features = {
            "previous_semester_marks": avg_internal_pct,
            "attendance_percentage": attendance_pct,
            "internal_examination_marks": avg_internal_pct,
            "assignment_completion_pct": assignment_pct,
            "practical_examination_marks": practical_pct,
            "classroom_participation": min(10.0, max(4.0, attendance_pct / 10.0)),
            "study_hours_per_day": 2.5
        }
        res = predict_student_performance(features)
        latest_pred = Prediction(
            student_id=student.id,
            predicted_percentage=res["predicted_percentage"],
            performance_category=res["performance_category"],
            risk_level=res["risk_level"],
            model_version=res["model_version"],
            weak_areas=res["weak_areas"],
            recommendations=res["recommendations"],
            input_features=str(features)
        )
        db.session.add(latest_pred)
        db.session.commit()

    return {
        "total_subjects": total_subjects,
        "attendance_pct": attendance_pct,
        "total_sessions": total_sessions,
        "attended_sessions": attended_sessions,
        "missed_sessions": missed_sessions,
        "avg_internal_pct": avg_internal_pct,
        "total_assignments": total_assignments,
        "completed_assignments": completed_assignments,
        "pending_assignments": pending_assignments,
        "assignment_pct": assignment_pct,
        "practical_pct": practical_pct,
        "predicted_score": float(latest_pred.predicted_percentage),
        "performance_category": latest_pred.performance_category,
        "risk_level": latest_pred.risk_level,
        "weak_areas": latest_pred.weak_areas,
        "recommendations": latest_pred.recommendations.split(" | ") if latest_pred.recommendations else []
    }

@student_bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    user = get_current_user()
    student = Student.query.filter_by(user_id=user.id).first()
    if not student:
        flash("Student profile not found. Please contact administration.", "danger")
        session.clear()
        return redirect(url_for("auth.login"))

    analytics = _compute_student_analytics(student)

    # Detailed collections
    marks_list = Mark.query.filter_by(student_id=student.id).order_by(Mark.exam_date.desc()).all()
    assignments = Assignment.query.filter_by(class_grade=student.class_grade).order_by(Assignment.due_date.asc()).all()
    submissions = {s.assignment_id: s for s in AssignmentSubmission.query.filter_by(student_id=student.id).all()}
    activities = Activity.query.filter_by(student_id=student.id).order_by(Activity.event_date.desc()).all()
    feedback_list = FacultyFeedback.query.filter_by(student_id=student.id).order_by(FacultyFeedback.created_at.desc()).all()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(8).all()

    # Chart data: Subject-wise marks
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
        "student_dashboard.html",
        student=student,
        analytics=analytics,
        marks_list=marks_list,
        assignments=assignments,
        submissions=submissions,
        activities=activities,
        feedback_list=feedback_list,
        notifications=notifications,
        chart_subjects=chart_subjects,
        chart_subject_scores=chart_subject_scores
    )

@student_bp.route("/simulate", methods=["POST"])
@login_required
@role_required("student")
def simulate():
    """Future Score Simulator API."""
    user = get_current_user()
    student = Student.query.filter_by(user_id=user.id).first()
    if not student:
        return jsonify({"success": False, "error": "Student profile not found"}), 404

    analytics = _compute_student_analytics(student)
    baseline = {
        "previous_semester_marks": analytics["avg_internal_pct"],
        "attendance_percentage": analytics["attendance_pct"],
        "internal_examination_marks": analytics["avg_internal_pct"],
        "assignment_completion_pct": analytics["assignment_pct"],
        "practical_examination_marks": analytics["practical_pct"],
        "classroom_participation": min(10.0, max(4.0, analytics["attendance_pct"] / 10.0)),
        "study_hours_per_day": 2.5
    }

    data = request.get_json() or {}
    hypothetical = {
        "internal_examination_marks": float(data.get("internal_marks", baseline["internal_examination_marks"])),
        "attendance_percentage": float(data.get("attendance", baseline["attendance_percentage"])),
        "assignment_completion_pct": float(data.get("assignment_pct", baseline["assignment_completion_pct"])),
        "practical_examination_marks": float(data.get("practical_marks", baseline["practical_examination_marks"])),
        "study_hours_per_day": float(data.get("study_hours", baseline["study_hours_per_day"]))
    }

    result = simulate_future_score(baseline, hypothetical)
    return jsonify(result)

@student_bp.route("/download-report")
@login_required
@role_required("student")
def download_report():
    user = get_current_user()
    student = Student.query.filter_by(user_id=user.id).first()
    analytics = _compute_student_analytics(student)
    marks_list = Mark.query.filter_by(student_id=student.id).all()
    feedback_list = FacultyFeedback.query.filter_by(student_id=student.id).all()

    from routes.report_generator import generate_student_pdf_report
    pdf_buffer = generate_student_pdf_report(student, analytics, marks_list, feedback_list)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"EduPredict_Report_{student.student_id}.pdf",
        mimetype="application/pdf"
    )
