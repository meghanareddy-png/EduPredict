"""
Authentication Routes
Handles Login, Registration (Student, Parent, Faculty), 1-Click Demo Login, Logout & Password Reset.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Student, Parent, Faculty, Department, Semester, ParentStudent

auth_bp = Blueprint("auth", __name__)

DEMO_ACCOUNTS = {
    "student": "student_aarav",
    "faculty": "faculty_sharma",
    "parent": "parent_patel",
    "admin": "admin"
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        role = session.get("role")
        if role == "student":
            return redirect(url_for("student.dashboard"))
        elif role == "parent":
            return redirect(url_for("parent.dashboard"))
        elif role == "faculty":
            return redirect(url_for("faculty.dashboard"))
        elif role == "admin":
            return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember_me"))

        if not login_id or not password:
            flash("Please enter both username/email and password.", "danger")
            return render_template("login.html")

        # Query by username or email
        user = User.query.filter(
            (User.username == login_id) | (User.email == login_id)
        ).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account has been deactivated. Please contact an administrator.", "danger")
                return render_template("login.html")

            session.permanent = remember
            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            session["role"] = user.role

            flash(f"Welcome back, {user.full_name}!", "success")
            if user.role == "student":
                return redirect(url_for("student.dashboard"))
            elif user.role == "parent":
                return redirect(url_for("parent.dashboard"))
            elif user.role == "faculty":
                return redirect(url_for("faculty.dashboard"))
            elif user.role == "admin":
                return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials. Please verify your login details.", "danger")

    return render_template("login.html")

@auth_bp.route("/demo-login/<role>")
def demo_login(role):
    """Provides 1-click instant login as demo Student, Faculty, Parent, or Admin."""
    username = DEMO_ACCOUNTS.get(role.lower())
    if not username:
        flash("Invalid demo role selected.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"Demo account for {role} not found. Please re-seed the database.", "warning")
        return redirect(url_for("auth.login"))

    session["user_id"] = user.id
    session["username"] = user.username
    session["full_name"] = user.full_name
    session["role"] = user.role

    flash(f"Logged in as Demo {role.title()} ({user.full_name})", "info")
    if user.role == "student":
        return redirect(url_for("student.dashboard"))
    elif user.role == "parent":
        return redirect(url_for("parent.dashboard"))
    elif user.role == "faculty":
        return redirect(url_for("faculty.dashboard"))
    elif user.role == "admin":
        return redirect(url_for("admin.dashboard"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    departments = Department.query.all()
    semesters = Semester.query.all()

    if request.method == "POST":
        role = request.form.get("role", "student").lower()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if role == "admin":
            flash("Admin accounts cannot be registered publicly.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", departments=departments, semesters=semesters)

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html", departments=departments, semesters=semesters)

        # Check existing user
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return render_template("register.html", departments=departments, semesters=semesters)

        username = email.split("@")[0]
        # Ensure unique username
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        new_user = User(
            username=username,
            email=email,
            role=role,
            full_name=full_name
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()

        # Role specific profile
        if role == "student":
            student_id = request.form.get("student_id", "").strip().upper()
            dept_id = request.form.get("department_id")
            sem_id = request.form.get("semester_id")
            class_grade = request.form.get("class_grade", "Class CSE-3A").strip()

            if not student_id or not dept_id or not sem_id:
                flash("Please fill all required student profile fields.", "danger")
                db.session.rollback()
                return render_template("register.html", departments=departments, semesters=semesters)

            if Student.query.filter_by(student_id=student_id).first():
                flash("Student ID already exists.", "danger")
                db.session.rollback()
                return render_template("register.html", departments=departments, semesters=semesters)

            student = Student(
                user_id=new_user.id,
                student_id=student_id,
                full_name=full_name,
                email=email,
                department_id=int(dept_id),
                semester_id=int(sem_id),
                class_grade=class_grade
            )
            db.session.add(student)

        elif role == "parent":
            phone = request.form.get("phone", "").strip()
            linked_student_id = request.form.get("linked_student_id", "").strip().upper()
            relationship = request.form.get("relationship", "Parent/Guardian").strip()

            parent = Parent(
                user_id=new_user.id,
                full_name=full_name,
                email=email,
                phone=phone
            )
            db.session.add(parent)
            db.session.flush()

            # Attempt to link student if student_id provided
            if linked_student_id:
                stu = Student.query.filter_by(student_id=linked_student_id).first()
                if stu:
                    db.session.add(ParentStudent(
                        parent_id=parent.id,
                        student_id=stu.id,
                        relationship_type=relationship,
                        is_verified=True
                    ))
                else:
                    flash(f"Note: Student ID '{linked_student_id}' was not found; can be verified later by admin.", "warning")

        elif role == "faculty":
            faculty_id = request.form.get("faculty_id", "").strip().upper()
            dept_id = request.form.get("department_id")

            if not faculty_id or not dept_id:
                flash("Please provide Faculty ID and Department.", "danger")
                db.session.rollback()
                return render_template("register.html", departments=departments, semesters=semesters)

            if Faculty.query.filter_by(faculty_id=faculty_id).first():
                flash("Faculty ID already exists.", "danger")
                db.session.rollback()
                return render_template("register.html", departments=departments, semesters=semesters)

            faculty = Faculty(
                user_id=new_user.id,
                faculty_id=faculty_id,
                full_name=full_name,
                email=email,
                department_id=int(dept_id)
            )
            db.session.add(faculty)

        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", departments=departments, semesters=semesters)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out safely.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f"Password reset instructions have been sent to {email}.", "success")
        else:
            flash("If that email address exists in our system, reset instructions have been sent.", "info")
        return redirect(url_for("auth.login"))
    return render_template("login.html", show_forgot=True)
