"""
Database Seeding Module
Initializes all database tables and seeds comprehensive demonstration data
with pre-configured accounts for Admin, Faculty, Student, and Parent.
"""

from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash
from models import (
    db, User, Department, Semester, Subject, FacultySubject, StudentSubject,
    Attendance, Mark, Assignment, AssignmentSubmission, Activity, Student,
    Parent, ParentStudent, Faculty, Prediction, FacultyFeedback, Notification
)

def seed_database(app):
    """Initializes tables and seeds initial data within the Flask app context."""
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("[EduPredict DB] Database already seeded. Skipping initial seeding.")
            return

        print("[EduPredict DB] Seeding initial academic data & users...")

        # 1. Departments
        dept_cse = Department(code="CSE", name="Computer Science & Engineering")
        dept_ece = Department(code="ECE", name="Electronics & Communication Engineering")
        dept_mech = Department(code="MECH", name="Mechanical Engineering")
        db.session.add_all([dept_cse, dept_ece, dept_mech])
        db.session.commit()

        # 2. Semesters
        sem5 = Semester(name="Semester 5", academic_year="2026-2027", is_current=True)
        sem6 = Semester(name="Semester 6", academic_year="2026-2027", is_current=False)
        db.session.add_all([sem5, sem6])
        db.session.commit()

        # 3. Subjects
        sub_algo = Subject(code="CS501", name="Design & Analysis of Algorithms", department_id=dept_cse.id, semester_id=sem5.id, credits=4)
        sub_dbms = Subject(code="CS502", name="Database Management Systems", department_id=dept_cse.id, semester_id=sem5.id, credits=4)
        sub_ml = Subject(code="CS503", name="Machine Learning & AI", department_id=dept_cse.id, semester_id=sem5.id, credits=4)
        sub_cn = Subject(code="CS504", name="Computer Networks", department_id=dept_cse.id, semester_id=sem5.id, credits=3)
        sub_web = Subject(code="CS505", name="Web Development Lab", department_id=dept_cse.id, semester_id=sem5.id, credits=2)
        db.session.add_all([sub_algo, sub_dbms, sub_ml, sub_cn, sub_web])
        db.session.commit()

        # 4. Users & Profiles

        # A. Admin
        u_admin = User(
            username="admin",
            email="admin@edupredict.edu",
            password_hash=generate_password_hash("AdminPass123!"),
            role="admin",
            full_name="System Administrator"
        )
        db.session.add(u_admin)
        db.session.commit()

        # B. Faculty (Prof. Rajesh Sharma)
        u_faculty = User(
            username="faculty_sharma",
            email="r.sharma@edupredict.edu",
            password_hash=generate_password_hash("FacultyPass123!"),
            role="faculty",
            full_name="Prof. Rajesh Sharma"
        )
        db.session.add(u_faculty)
        db.session.commit()

        fac_sharma = Faculty(
            user_id=u_faculty.id,
            faculty_id="FAC101",
            full_name="Prof. Rajesh Sharma",
            email="r.sharma@edupredict.edu",
            department_id=dept_cse.id
        )
        db.session.add(fac_sharma)
        db.session.commit()

        # Assign Faculty to Subjects for Class CSE-3A
        for sub in [sub_algo, sub_dbms, sub_ml]:
            db.session.add(FacultySubject(
                faculty_id=fac_sharma.id,
                subject_id=sub.id,
                class_grade="Class CSE-3A",
                academic_year="2026-2027"
            ))
        db.session.commit()

        # C. Students
        # Student 1: Aarav Patel (On Track / Distinction)
        u_stu1 = User(
            username="student_aarav",
            email="aarav.patel@student.edu",
            password_hash=generate_password_hash("StudentPass123!"),
            role="student",
            full_name="Aarav Patel"
        )
        # Student 2: Priya Singh (Needs Attention / Second Class)
        u_stu2 = User(
            username="student_priya",
            email="priya.singh@student.edu",
            password_hash=generate_password_hash("PriyaPass123!"),
            role="student",
            full_name="Priya Singh"
        )
        # Student 3: Rohan Verma (High Support Priority / Remedial)
        u_stu3 = User(
            username="student_rohan",
            email="rohan.verma@student.edu",
            password_hash=generate_password_hash("RohanPass123!"),
            role="student",
            full_name="Rohan Verma"
        )
        db.session.add_all([u_stu1, u_stu2, u_stu3])
        db.session.commit()

        s1 = Student(user_id=u_stu1.id, student_id="STU1001", full_name="Aarav Patel", email=u_stu1.email, department_id=dept_cse.id, semester_id=sem5.id, class_grade="Class CSE-3A")
        s2 = Student(user_id=u_stu2.id, student_id="STU1002", full_name="Priya Singh", email=u_stu2.email, department_id=dept_cse.id, semester_id=sem5.id, class_grade="Class CSE-3A")
        s3 = Student(user_id=u_stu3.id, student_id="STU1003", full_name="Rohan Verma", email=u_stu3.email, department_id=dept_cse.id, semester_id=sem5.id, class_grade="Class CSE-3A")
        db.session.add_all([s1, s2, s3])
        db.session.commit()

        # Enroll students in all subjects
        for s in [s1, s2, s3]:
            for sub in [sub_algo, sub_dbms, sub_ml, sub_cn, sub_web]:
                db.session.add(StudentSubject(student_id=s.id, subject_id=sub.id, semester_id=sem5.id))
        db.session.commit()

        # D. Parents
        # Parent 1 (Suresh Patel -> Aarav)
        u_par1 = User(
            username="parent_patel",
            email="suresh.patel@family.org",
            password_hash=generate_password_hash("ParentPass123!"),
            role="parent",
            full_name="Suresh Patel"
        )
        # Parent 2 (Sunita Singh -> Priya)
        u_par2 = User(
            username="parent_singh",
            email="sunita.singh@family.org",
            password_hash=generate_password_hash("ParentPass123!"),
            role="parent",
            full_name="Sunita Singh"
        )
        db.session.add_all([u_par1, u_par2])
        db.session.commit()

        par1 = Parent(user_id=u_par1.id, full_name="Suresh Patel", email=u_par1.email, phone="+91 98765 43210")
        par2 = Parent(user_id=u_par2.id, full_name="Sunita Singh", email=u_par2.email, phone="+91 98765 43211")
        db.session.add_all([par1, par2])
        db.session.commit()

        # Verified Parent-Student links
        db.session.add(ParentStudent(parent_id=par1.id, student_id=s1.id, relationship_type="Father", is_verified=True))
        db.session.add(ParentStudent(parent_id=par2.id, student_id=s2.id, relationship_type="Mother", is_verified=True))
        db.session.commit()

        # 5. Attendance Records
        today = date.today()
        # Student 1: High attendance (~92%)
        for i in range(25):
            d = today - timedelta(days=i)
            st_status = "Present" if i % 12 != 0 else "Absent"
            for sub in [sub_algo, sub_dbms, sub_ml]:
                db.session.add(Attendance(
                    student_id=s1.id, subject_id=sub.id, date=d, status=st_status,
                    total_sessions=1, attended_sessions=1 if st_status == "Present" else 0,
                    recorded_by=fac_sharma.id
                ))
        # Student 2: Moderate attendance (~72%)
        for i in range(25):
            d = today - timedelta(days=i)
            st_status = "Present" if i % 4 != 0 else "Absent"
            for sub in [sub_algo, sub_dbms, sub_ml]:
                db.session.add(Attendance(
                    student_id=s2.id, subject_id=sub.id, date=d, status=st_status,
                    total_sessions=1, attended_sessions=1 if st_status == "Present" else 0,
                    recorded_by=fac_sharma.id
                ))
        # Student 3: Low attendance (~56%)
        for i in range(25):
            d = today - timedelta(days=i)
            st_status = "Present" if i % 2 == 0 else "Absent"
            for sub in [sub_algo, sub_dbms, sub_ml]:
                db.session.add(Attendance(
                    student_id=s3.id, subject_id=sub.id, date=d, status=st_status,
                    total_sessions=1, attended_sessions=1 if st_status == "Present" else 0,
                    recorded_by=fac_sharma.id
                ))
        db.session.commit()

        # 6. Marks Records
        # Student 1: Aarav (High scores ~88%)
        marks_data_s1 = [
            (sub_algo, "Internal 1", 46.0, 50.0),
            (sub_algo, "Internal 2", 48.0, 50.0),
            (sub_dbms, "Internal 1", 44.0, 50.0),
            (sub_dbms, "Internal 2", 45.0, 50.0),
            (sub_ml, "Internal 1", 47.0, 50.0),
            (sub_ml, "Practical", 48.0, 50.0),
        ]
        for sub, etype, obt, maxm in marks_data_s1:
            db.session.add(Mark(student_id=s1.id, subject_id=sub.id, exam_type=etype, marks_obtained=obt, max_marks=maxm, exam_date=today - timedelta(days=10), recorded_by=fac_sharma.id))

        # Student 2: Priya (Moderate scores ~68%)
        marks_data_s2 = [
            (sub_algo, "Internal 1", 34.0, 50.0),
            (sub_algo, "Internal 2", 33.0, 50.0),
            (sub_dbms, "Internal 1", 36.0, 50.0),
            (sub_dbms, "Internal 2", 35.0, 50.0),
            (sub_ml, "Internal 1", 31.0, 50.0),
            (sub_ml, "Practical", 38.0, 50.0),
        ]
        for sub, etype, obt, maxm in marks_data_s2:
            db.session.add(Mark(student_id=s2.id, subject_id=sub.id, exam_type=etype, marks_obtained=obt, max_marks=maxm, exam_date=today - timedelta(days=10), recorded_by=fac_sharma.id))

        # Student 3: Rohan (Low scores ~52%)
        marks_data_s3 = [
            (sub_algo, "Internal 1", 24.0, 50.0),
            (sub_algo, "Internal 2", 22.0, 50.0),
            (sub_dbms, "Internal 1", 26.0, 50.0),
            (sub_dbms, "Internal 2", 25.0, 50.0),
            (sub_ml, "Internal 1", 20.0, 50.0),
            (sub_ml, "Practical", 28.0, 50.0),
        ]
        for sub, etype, obt, maxm in marks_data_s3:
            db.session.add(Mark(student_id=s3.id, subject_id=sub.id, exam_type=etype, marks_obtained=obt, max_marks=maxm, exam_date=today - timedelta(days=10), recorded_by=fac_sharma.id))
        db.session.commit()

        # 7. Assignments & Submissions
        asg1 = Assignment(
            subject_id=sub_algo.id,
            faculty_id=fac_sharma.id,
            title="Dynamic Programming: Knapsack & Matrix Chain",
            description="Implement bottom-up DP solutions with asymptotic time complexity proofs.",
            max_marks=100.0,
            due_date=datetime.now() + timedelta(days=5),
            class_grade="Class CSE-3A"
        )
        asg2 = Assignment(
            subject_id=sub_dbms.id,
            faculty_id=fac_sharma.id,
            title="Relational Schema Normalization & BCNF",
            description="Analyze functional dependencies and synthesize 3NF and BCNF decomposed tables.",
            max_marks=100.0,
            due_date=datetime.now() + timedelta(days=8),
            class_grade="Class CSE-3A"
        )
        asg3 = Assignment(
            subject_id=sub_ml.id,
            faculty_id=fac_sharma.id,
            title="Linear & Logistic Regression Pipeline",
            description="Train scikit-learn models on housing and diagnostic datasets with cross-validation.",
            max_marks=100.0,
            due_date=datetime.now() - timedelta(days=2),
            class_grade="Class CSE-3A"
        )
        db.session.add_all([asg1, asg2, asg3])
        db.session.commit()

        # Submissions
        db.session.add(AssignmentSubmission(assignment_id=asg1.id, student_id=s1.id, submission_text="GitHub repository link submitted with test suite.", marks_obtained=95.0, is_completed=True, feedback="Exceptional algorithmic complexity proof."))
        db.session.add(AssignmentSubmission(assignment_id=asg2.id, student_id=s1.id, submission_text="SQL schema design doc and relational decomposition submitted.", marks_obtained=92.0, is_completed=True, feedback="Very thorough BCNF synthesis."))
        db.session.add(AssignmentSubmission(assignment_id=asg3.id, student_id=s1.id, submission_text="Python notebook with cross-validation results attached.", marks_obtained=96.0, is_completed=True, feedback="Outstanding model evaluation graphs."))

        db.session.add(AssignmentSubmission(assignment_id=asg1.id, student_id=s2.id, submission_text="Submitted code for 0/1 knapsack.", marks_obtained=74.0, is_completed=True, feedback="Good effort, review Matrix Chain multiplication boundary cases."))
        db.session.add(AssignmentSubmission(assignment_id=asg3.id, student_id=s2.id, submission_text="Regression models submitted.", marks_obtained=70.0, is_completed=True, feedback="Ensure hyperparameter tuning is documented."))

        db.session.add(AssignmentSubmission(assignment_id=asg1.id, student_id=s3.id, submission_text="Partial submission.", marks_obtained=45.0, is_completed=True, feedback="Missing memoization implementation."))
        db.session.commit()

        # 8. Student Activities
        db.session.add(Activity(student_id=s1.id, activity_type="Technical Event", title="National Hackathon 2026 - 1st Place", description="Built decentralized AI data pipeline; awarded ₹50,000 cash prize.", achievement_level="Winner", event_date=today - timedelta(days=20)))
        db.session.add(Activity(student_id=s1.id, activity_type="Certification", title="AWS Certified Cloud Practitioner", description="Scored 920/1000 in official AWS Cloud Practitioner examination.", achievement_level="Certified", event_date=today - timedelta(days=40)))
        db.session.add(Activity(student_id=s2.id, activity_type="Workshop", title="Hands-on Cloud Computing with Docker", description="Completed 16-hour intensive containerization workshop.", achievement_level="Completed", event_date=today - timedelta(days=15)))
        db.session.add(Activity(student_id=s3.id, activity_type="Sports", title="Inter-College Football Tournament", description="Represented university as center forward in zonal tournament.", achievement_level="Runner Up", event_date=today - timedelta(days=25)))
        db.session.commit()

        # 9. AI Predictions
        db.session.add(Prediction(
            student_id=s1.id,
            predicted_percentage=90.5,
            performance_category="Distinction",
            risk_level="Low",
            model_version="v1.0-rf-regressor",
            weak_areas="None. Exceptional consistency across all subjects.",
            recommendations="Maintain daily study schedule | Explore advanced research internships | Mentor peers in Algorithms",
            input_features='{"attendance_pct": 92.0, "internal_pct": 91.5, "assignment_pct": 94.3, "study_hours": 4.5, "previous_score": 88.0}'
        ))
        db.session.add(Prediction(
            student_id=s2.id,
            predicted_percentage=72.0,
            performance_category="Second Class",
            risk_level="Medium",
            model_version="v1.0-rf-regressor",
            weak_areas="Design & Analysis of Algorithms, Machine Learning theory",
            recommendations="Increase attendance to >= 80% | Schedule weekly faculty consultation for Algorithms | Dedicate 1.5 extra study hours daily",
            input_features='{"attendance_pct": 72.0, "internal_pct": 68.0, "assignment_pct": 72.0, "study_hours": 2.5, "previous_score": 70.0}'
        ))
        db.session.add(Prediction(
            student_id=s3.id,
            predicted_percentage=54.5,
            performance_category="Remedial",
            risk_level="High",
            model_version="v1.0-rf-regressor",
            weak_areas="Database Management Systems, Algorithms, Computer Networks",
            recommendations="Immediate mandatory attendance counseling | Peer tutoring assignment | Submit all pending homework assignments",
            input_features='{"attendance_pct": 56.0, "internal_pct": 49.0, "assignment_pct": 45.0, "study_hours": 1.5, "previous_score": 58.0}'
        ))
        db.session.commit()

        # 10. Faculty Feedback
        db.session.add(FacultyFeedback(student_id=s1.id, faculty_id=fac_sharma.id, feedback_text="Aarav continues to demonstrate top-tier performance. His problem-solving rigor is exemplary.", category="Academic Excellence"))
        db.session.add(FacultyFeedback(student_id=s2.id, faculty_id=fac_sharma.id, feedback_text="Priya has high potential but misses classes occasionally. With regular attendance, her marks will jump significantly.", category="Improvement Needed"))
        db.session.add(FacultyFeedback(student_id=s3.id, faculty_id=fac_sharma.id, feedback_text="Rohan needs immediate remedial support in Algorithms and DBMS. Please attend office hours this week.", category="Critical Intervention"))
        db.session.commit()

        # 11. Notifications
        # Notifications for Student 1
        db.session.add(Notification(user_id=u_stu1.id, title="High Performance Recognition", message="Congratulations! Your predicted trajectory puts you in the Distinction tier (&gt; 90%). Keep up the great work!", notification_type="Marks", is_read=False))
        db.session.add(Notification(user_id=u_stu1.id, title="New Assignment Uploaded", message="Assignment 2 for DBMS (Normalization & BCNF) is due in 8 days.", notification_type="Assignment", is_read=True))

        # Notifications for Student 2
        db.session.add(Notification(user_id=u_stu2.id, title="Attendance Notice", message="Your attendance is currently at 72%. Please attend upcoming classes to reach the institutional benchmark of >= 75%.", notification_type="Attendance", is_read=False))

        # Notifications for Student 3
        db.session.add(Notification(user_id=u_stu3.id, title="Academic Support Alert", message="Your predicted trajectory requires immediate faculty guidance. Please meet Prof. Sharma for assistance.", notification_type="Exam", is_read=False))

        # Notifications for Parent 1
        db.session.add(Notification(user_id=u_par1.id, title="Student Progress Update", message="Aarav Patel has achieved a 92% attendance rate and is on track for Distinction honors.", notification_type="General", is_read=False))

        # Notifications for Parent 2
        db.session.add(Notification(user_id=u_par2.id, title="Attendance Alert for Priya", message="Priya's attendance is currently 72%, below the recommended 75% threshold. Please review her schedule.", notification_type="Attendance", is_read=False))

        db.session.commit()
        print("[EduPredict DB] Seeding completed successfully!")
