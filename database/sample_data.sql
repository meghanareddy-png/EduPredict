-- ============================================================================
-- EduPredict MySQL 8.0 Sample Data Seeding
-- Populates complete demonstration environment with pre-hashed bcrypt credentials
-- ============================================================================

USE edupredict_db;

-- 1. Departments
INSERT IGNORE INTO departments (id, code, name) VALUES
(1, 'CSE', 'Computer Science & Engineering'),
(2, 'ECE', 'Electronics & Communication Engineering'),
(3, 'MECH', 'Mechanical Engineering');

-- 2. Semesters
INSERT IGNORE INTO semesters (id, name, academic_year, is_current) VALUES
(1, 'Semester 5', '2026-2027', TRUE),
(2, 'Semester 6', '2026-2027', FALSE);

-- 3. Subjects
INSERT IGNORE INTO subjects (id, code, name, department_id, semester_id, credits) VALUES
(1, 'CS501', 'Design & Analysis of Algorithms', 1, 1, 4),
(2, 'CS502', 'Database Management Systems', 1, 1, 4),
(3, 'CS503', 'Machine Learning & AI', 1, 1, 4),
(4, 'CS504', 'Computer Networks', 1, 1, 3),
(5, 'CS505', 'Web Development Lab', 1, 1, 2);

-- Note: User accounts with secure pbkdf2/bcrypt password hashes are initialized
-- automatically via Python `database/seed.py` for guaranteed cross-platform hash compatibility.
