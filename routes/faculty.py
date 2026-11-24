"""
Faculty Dashboard Routes & Functionalities
"""

from datetime import datetime, date
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, send_file
from models import (
    db, Faculty, FacultySubject, Subject, Student, StudentSubject,
    Attendance, Mark, Assignment, AssignmentSubmission, Activity,
    FacultyFeedback, Notification, Prediction
)
from routes.helpers import login_required, role_required, get_current_user
from routes.student import _compute_student_analytics

faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")

@faculty_bp.route("/dashboard")
@login_required
@role_required("faculty")
def dashboard():
    user = get_current_user()
    faculty = Faculty.query.filter_by(user_id=user.id).first()
    if not faculty:
        flash("Faculty profile not found.", "danger")
        return redirect(url_for("auth.login"))

    # Assigned subjects & classes
    assignments = FacultySubject.query.filter_by(faculty_id=faculty.id).all()
    assigned_classes = list(set(a.class_grade for a in assignments))
    assigned_subjects = [a.subject for a in assignments]

    # Selected class filter
    selected_class = request.args.get("class_grade")
    if not selected_class and assigned_classes:
        selected_class = assigned_classes[0]

    # Enrolled students in class
    if selected_class:
        students = Student.query.filter_by(class_grade=selected_class).all()
    else:
        students = Student.query.all()

    # Search & status filter
    search_query = request.args.get("q", "").strip().lower()
    risk_filter = request.args.get("risk", "all")

    student_data = []
    low_attendance_count = 0
    at_risk_count = 0
    total_class_score = 0

    for s in students:
        analytics = _compute_student_analytics(s)
        if analytics["attendance_pct"] < 75.0:
            low_attendance_count += 1
        if analytics["risk_level"] in ("Medium", "High"):
            at_risk_count += 1
        total_class_score += analytics["predicted_score"]

        # Filter check
        matches_search = (search_query in s.full_name.lower() or search_query in s.student_id.lower()) if search_query else True
        matches_risk = (risk_filter == "all" or analytics["risk_level"].lower() == risk_filter.lower())
        
        if matches_search and matches_risk:
            student_data.append({
                "student": s,
                "analytics": analytics
            })

    avg_class_perf = round(total_class_score / len(students), 1) if students else 0.0

    # Assignment statistics
    faculty_assignments = Assignment.query.filter_by(faculty_id=faculty.id).all()

    return render_template(
        "faculty_dashboard.html",
        faculty=faculty,
        assigned_classes=assigned_classes,
        selected_class=selected_class,
        assigned_subjects=assigned_subjects,
        student_data=student_data,
        total_students=len(students),
        total_subjects=len(assigned_subjects),
        avg_class_perf=avg_class_perf,
        low_attendance_count=low_attendance_count,
        at_risk_count=at_risk_count,
        faculty_assignments=faculty_assignments,
        search_query=search_query,
        risk_filter=risk_filter
    )

@faculty_bp.route("/add-marks", methods=["POST"])
@login_required
@role_required("faculty")
def add_marks():
    user = get_current_user()
    faculty = Faculty.query.filter_by(user_id=user.id).first()

    student_id = request.form.get("student_id")
    subject_id = request.form.get("subject_id")
    exam_type = request.form.get("exam_type", "Internal Examination")
    marks_obtained = float(request.form.get("marks_obtained", 0))
    max_marks = float(request.form.get("max_marks", 100))
    remarks = request.form.get("remarks", "")

    new_mark = Mark(
        student_id=int(student_id),
        subject_id=int(subject_id),
        exam_type=exam_type,
        marks_obtained=marks_obtained,
        max_marks=max_marks,
        exam_date=date.today(),
        recorded_by=faculty.id,
        remarks=remarks
    )
    db.session.add(new_mark)

    # Invalidate old prediction so live model recalculates
    Prediction.query.filter_by(student_id=int(student_id)).delete()

    db.session.commit()
    flash("Academic mark recorded successfully. AI trajectory updated.", "success")
    return redirect(request.referrer or url_for("faculty.dashboard"))

@faculty_bp.route("/update-attendance", methods=["POST"])
@login_required
@role_required("faculty")
def update_attendance():
    user = get_current_user()
    faculty = Faculty.query.filter_by(user_id=user.id).first()

    student_id = request.form.get("student_id")
    subject_id = request.form.get("subject_id")
    status = request.form.get("status", "Present")

    att = Attendance(
        student_id=int(student_id),
        subject_id=int(subject_id),
        date=date.today(),
        status=status,
        total_sessions=1,
        attended_sessions=1 if status == "Present" else 0,
        recorded_by=faculty.id
    )
    db.session.add(att)

    # Trigger attendance warning notification if low
    stu = Student.query.get(int(student_id))
    analytics = _compute_student_analytics(stu)
    if analytics["attendance_pct"] < 75.0:
        db.session.add(Notification(
            user_id=stu.user_id,
            title="Attendance Warning",
            message=f"Your overall attendance is {analytics['attendance_pct']}%, which is below the required 75%.",
            notification_type="Attendance"
        ))

    db.session.commit()
    flash("Attendance logged successfully.", "success")
    return redirect(request.referrer or url_for("faculty.dashboard"))

@faculty_bp.route("/add-assignment", methods=["POST"])
@login_required
@role_required("faculty")
def add_assignment():
    user = get_current_user()
    faculty = Faculty.query.filter_by(user_id=user.id).first()

    subject_id = request.form.get("subject_id")
    title = request.form.get("title")
    description = request.form.get("description")
    max_marks = float(request.form.get("max_marks", 100))
    due_date_str = request.form.get("due_date")
    class_grade = request.form.get("class_grade")

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else datetime.now()

    asg = Assignment(
        subject_id=int(subject_id),
        faculty_id=faculty.id,
        title=title,
        description=description,
        max_marks=max_marks,
        due_date=due_date,
        class_grade=class_grade
    )
    db.session.add(asg)

    # Notify enrolled students
    students = Student.query.filter_by(class_grade=class_grade).all()
    for s in students:
        db.session.add(Notification(
            user_id=s.user_id,
            title=f"New Assignment: {title}",
            message=f"Due on {due_date.strftime('%b %d, %Y')}. Max Marks: {max_marks}.",
            notification_type="Assignment"
        ))

    db.session.commit()
    flash("Assignment uploaded and notified to all enrolled students.", "success")
    return redirect(request.referrer or url_for("faculty.dashboard"))

@faculty_bp.route("/feedback", methods=["POST"])
@login_required
@role_required("faculty")
def give_feedback():
    user = get_current_user()
    faculty = Faculty.query.filter_by(user_id=user.id).first()

    student_id = request.form.get("student_id")
    feedback_text = request.form.get("feedback_text")
    category = request.form.get("category", "Academic Progress")

    fb = FacultyFeedback(
        student_id=int(student_id),
        faculty_id=faculty.id,
        feedback_text=feedback_text,
        category=category
    )
    db.session.add(fb)

    # Notify student
    stu = Student.query.get(int(student_id))
    db.session.add(Notification(
        user_id=stu.user_id,
        title="New Faculty Feedback",
        message=f"{faculty.full_name} provided feedback: '{feedback_text}'",
        notification_type="Feedback"
    ))

    db.session.commit()
    flash(f"Personalized feedback shared with {stu.full_name}.", "success")
    return redirect(request.referrer or url_for("faculty.dashboard"))

@faculty_bp.route("/student-profile/<int:student_id>")
@login_required
@role_required("faculty")
def student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    analytics = _compute_student_analytics(student)
    marks_list = Mark.query.filter_by(student_id=student.id).order_by(Mark.exam_date.desc()).all()
    activities = Activity.query.filter_by(student_id=student.id).all()
    feedback_list = FacultyFeedback.query.filter_by(student_id=student.id).all()

    return render_template(
        "student_profile_modal.html",
        student=student,
        analytics=analytics,
        marks_list=marks_list,
        activities=activities,
        feedback_list=feedback_list
    )
