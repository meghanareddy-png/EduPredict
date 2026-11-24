<p align="center">
  <img src="static/images/edupredict-logo.png" alt="EduPredict Logo" width="380">
</p>

<h1 align="center">EduPredict</h1>
<h3 align="center">AI-Powered Student Academic Performance Prediction and Monitoring System</h3>
<p align="center"><b><em>"Predict. Perform. Progress."</em></b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=flat&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--Learn-1.6-F7931E?style=flat&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Chart.js-4.4-FF6384?style=flat&logo=chartdotjs&logoColor=white" alt="Chart.js">
  <img src="https://img.shields.io/badge/Tests-11%20Passed-16A34A?style=flat&logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-7C3AED?style=flat" alt="Status">
</p>

---

## 📌 Executive Summary

**EduPredict** is an enterprise-grade educational SaaS platform designed to bridge the gap between academic monitoring, early risk intervention, and proactive student mentorship. Connecting **Students**, **Parents**, **Faculty**, and **Administrators** in one cohesive ecosystem, EduPredict utilizes trained Machine Learning models (Random Forest, Decision Trees, and Logistic Regression) to assess academic trajectories, identify individual learning gaps, deliver personalized recommendations, and empower students to simulate their future scores through an interactive slider engine.

---

## 🎨 Brand Identity & Design System

EduPredict adheres to a commercial, modern AI dashboard design system with soft elevation shadows, rounded cards, and smooth transitions:

| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Primary Purple** | `#7C3AED` | Primary brand accent, hero CTA buttons, active state highlights |
| **Dark Purple** | `#4C1D95` | Brand typography headings, splash gradient, sidebars |
| **Background** | `#F5F3FF` | Clean, modern page background tone |
| **Accent Purple** | `#A78BFA` | Sub-headings, borders, badge backgrounds |
| **Card Background** | `#FFFFFF` | Elevated dashboard containers and KPI cards |
| **Main Text** | `#1E1B4B` | High-contrast readable body typography |
| **Success Green** | `#16A34A` | Low-risk indicators, passing thresholds, high attendance |
| **Warning Orange** | `#F59E0B` | Medium-risk alerts, pending assignments |
| **Danger Red** | `#DC2626` | High-risk alerts, attendance warnings (<75%), failed submissions |

---

## 🚀 Key Modules & Capabilities

### 1. 🎬 Animated Splash Screen
- **Full-Screen Experience**: Centered EduPredict logo with radial glowing effect over dark purple gradient (`#4C1D95` to `#7C3AED`).
- **Initial Visit Retention**: Automatically displays for **exactly 3 seconds** on first visit and fades out smoothly; suppresses repeat shows during session navigation using `sessionStorage`.

### 2. 🌐 Modern SaaS Landing Page
- **Hero Showcase**: Value proposition with dynamic 1-click demo launchers.
- **5-Step Operational Flow**:
  1. *Collect Academic Information*
  2. *Analyze Student Performance*
  3. *Predict Future Outcomes*
  4. *Generate Personalized Recommendations*
  5. *Monitor Continuous Improvement*
- **Feature Matrix & FAQ**: Real-time analytics, parental oversight, faculty gradebook, and security overview.

### 3. 🔐 Enterprise RBAC Authentication
- Four distinct roles: **Student**, **Parent**, **Faculty**, and **Administrator**.
- PBKDF2-SHA256 password hashing via Werkzeug security.
- Flask session authorization with route-level role-guard decorators (`@login_required`, `@role_required`).

### 4. 🎓 Student Dashboard
- **Dynamic KPI Tiles**: Total Subjects, Attendance %, Internal Marks Average, Assignment Completion %, Predicted Score, Risk Level.
- **Interactive "Future Score Simulator"**: Real-time sliders allowing students to test hypothetical attendance, internal marks, and study hours to visualize outcome impact before final exams.
- **Subject-Wise Mark Breakdown & Attendance Trajectory Charts**: Powered by Chart.js.
- **Institutional PDF Progress Report**: One-click download of an official academic summary generated on-the-fly with ReportLab.

### 5. 👨‍👩‍👧 Parent Dashboard
- **Linked Child Monitoring**: Multi-child switcher allowing parents to monitor each linked student's performance independently.
- **At-a-Glance Alerts**: Real-time badges for attendance warnings (<75%), upcoming assignment deadlines, and faculty remarks.
- **Actionable Home Support Tips**: Automatically generated suggestions on how parents can assist their child's academic weaknesses.

### 6. 👨‍🏫 Faculty Dashboard
- **Class Cohort Metrics**: Average marks, low attendance counts, and at-risk student count.
- **Searchable Roster & Gradebook**: Add internal examination marks, record daily attendance sessions, and upload assignments.
- **Mentorship Feedback**: Submit constructive pedagogical notes directly to student and parent dashboards.

### 7. 🛡️ Administrator Panel
- **Institutional Management**: Departments, semesters, subjects, and faculty-to-course allocations.
- **Parent-Student Relationship Verification**: Review and approve guardian linkages.
- **ML Governance**: One-click ML model retraining, evaluation metrics inspection ($R^2$, MAE, Accuracy), and campus-wide announcement broadcast.

---

## 🤖 Machine Learning Architecture

EduPredict employs a multi-model ensemble built on **Scikit-learn**:

```
Features Input Vector (7 Attributes)
├── Previous Semester Marks (%)
├── Current Attendance Percentage (%)
├── Internal Examination Marks (%)
├── Assignment Completion (%)
├── Practical Lab Exam Marks (%)
├── Classroom Participation Rating (1 - 10)
└── Daily Self-Study Hours (0.5 - 8.0)
       │
       ├──► [Random Forest Regressor]    ──► Predicted Academic Score (e.g., 84.7%)
       │
       ├──► [Decision Tree Classifier]   ──► Academic Category (Distinction / First Class / Second Class / Remedial)
       │
       └──► [Logistic Regression (Scaled)]─► Academic Risk Level (Low / Medium / High)
```

### Model Performance Metrics (Validated via Pytest)
- **Random Forest Regressor**: $R^2 = 0.9145$, $\text{MAE} = 2.49\%$
- **Decision Tree Classifier**: Accuracy $= 79.00\%$
- **Logistic Regression Risk Classifier**: Accuracy $= 93.00\%$
- **Pedagogical Recommendation Engine**: Rule-based weakness detection generating personalized academic advice tailored to individual deficiency areas.

---

## 🔑 Demo Accounts & Pre-Seeded Credentials

You can instantly log in with any of the following pre-configured demonstration accounts or use the **1-Click Demo Login** buttons on the login page:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| 🛡️ **Administrator** | `admin` | `AdminPass123!` | System settings, user directory, ML retrain |
| 👨‍🏫 **Faculty** | `faculty_sharma` | `FacultyPass123!` | CSE Dept, marks entry, attendance management |
| 🎓 **Student** | `student_aarav` | `StudentPass123!` | 3rd Year CSE, high performance, score simulator |
| 👨‍👩‍👧 **Parent** | `parent_patel` | `ParentPass123!` | Linked to student Aarav Patel |

---

## ⚙️ Quickstart & Local Installation

### Prerequisites
- **Python 3.10+** (Tested on Python 3.14)
- **Git**
- *(Optional)* MySQL Server 8.0 (System automatically defaults to zero-configuration SQLite if MySQL is offline)

### Step 1: Clone the Repository
```bash
git clone https://github.com/meghanareddy-png/EduPredict.git
cd EduPredict
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access in Browser
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🗄️ Database Architecture

EduPredict includes production-ready schemas for **MySQL 8.0** with automatic fallback to **SQLite**:
- `database/schema.sql`: Complete DDL creating 18 relational tables with foreign keys and cascade rules.
- `database/sample_data.sql`: Seed data for departments, semesters, and course curriculums.
- `database/seed.py`: Automated programmatic seeder populating users, test marks, assignments, and sample attendance logs.

To configure MySQL in production, create a `.env` file from `.env.example`:
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=edupredict_db
SECRET_KEY=your_secure_secret_key_here
PORT=5000
```

---

## 🧪 Automated Test Suite

EduPredict includes unit and integration tests across authentication, database integrity, and machine learning inference:

```bash
python -m pytest tests/ -v
```

**Results: 11 of 11 tests passing (100%):**
- `test_user_password_hashing`: Password encryption & PBKDF2 validation
- `test_login_flow`: Valid/invalid credentials & session lifecycle
- `test_demo_logins`: 1-Click demo authentication across all 4 roles
- `test_logout`: Safe session invalidation
- `test_student_and_academic_creation`: Student profiles, marks, and attendance records
- `test_parent_child_relationship`: Relational guardian mapping
- `test_ml_prediction_inference`: Scikit-learn inference pipeline
- `test_high_risk_prediction`: Low score weakness detection and faculty intervention flags
- `test_future_score_simulator`: Trajectory delta calculation
- `test_api_predict_endpoint`: REST API `/api/prediction/predict`
- `test_api_simulate_endpoint`: REST API `/api/prediction/simulate`

---

## 🌐 Note on Hosting (Localhost vs. GitHub Pages)

> [!NOTE]
> **Why doesn't EduPredict run directly on GitHub Pages?**
> GitHub Pages (`meghanareddy-png.github.io/EduPredict/`) is a **static web host** intended only for static HTML, CSS, client-side JS, and Markdown files. 
> 
> EduPredict is a **full-stack application** with an active Python runtime, Flask web server, relational database (MySQL/SQLite), and Scikit-learn Machine Learning inference models. It requires a live Python runtime to process authentication, run predictions, and serve dynamic data.
>
> To deploy EduPredict live on the public internet, deploy this repository to a cloud application platform such as:
> - **Render** (Web Service, `python app.py` or `gunicorn app:app`)
> - **Railway**
> - **PythonAnywhere**
> - **Heroku / AWS Elastic Beanstalk**

---

<p align="center">
  <b>EduPredict &copy; 2026 &bull; Predict. Perform. Progress.</b>
</p>
