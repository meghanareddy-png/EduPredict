"""
EduPredict Machine Learning Dataset Generator
Generates a realistic, statistically grounded dataset of 1,000 student academic profiles
with realistic collinearity and noise for rigorous model training and evaluation.
"""

import os
import numpy as np
import pandas as pd

def generate_dataset(num_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    # 1. Previous Semester Marks (40 - 98)
    prev_marks = np.random.normal(loc=72, scale=14, size=num_samples)
    prev_marks = np.clip(prev_marks, 40, 99)

    # 2. Attendance Percentage (correlated with discipline)
    att_noise = np.random.normal(loc=0, scale=8, size=num_samples)
    attendance = 0.55 * prev_marks + 38 + att_noise
    attendance = np.clip(attendance, 45, 100)

    # 3. Current Internal Marks (correlated with attendance & previous)
    int_noise = np.random.normal(loc=0, scale=6, size=num_samples)
    internal_marks = 0.45 * prev_marks + 0.35 * attendance + 14 + int_noise
    internal_marks = np.clip(internal_marks, 35, 100)

    # 4. Assignment Completion Percentage
    assign_noise = np.random.normal(loc=0, scale=7, size=num_samples)
    assignment_pct = 0.60 * attendance + 0.25 * internal_marks + assign_noise
    assignment_pct = np.clip(assignment_pct, 40, 100)

    # 5. Practical Examination Marks
    prac_noise = np.random.normal(loc=0, scale=6, size=num_samples)
    practical_marks = 0.50 * internal_marks + 0.30 * assignment_pct + 15 + prac_noise
    practical_marks = np.clip(practical_marks, 40, 100)

    # 6. Classroom Participation (Score 1 - 10)
    part_raw = 0.05 * attendance + 0.04 * internal_marks + np.random.normal(0, 1.2, num_samples)
    participation = np.clip(np.round(part_raw, 1), 1.0, 10.0)

    # 7. Daily Study Hours (0.5 to 8.0)
    hours_raw = 0.04 * prev_marks + 0.03 * internal_marks - 1.2 + np.random.normal(0, 0.7, num_samples)
    study_hours = np.clip(np.round(hours_raw, 1), 0.5, 8.0)

    # 8. Target: Final Academic Percentage
    # Weighted ground truth formula with realistic variance
    final_score = (
        0.35 * internal_marks +
        0.25 * prev_marks +
        0.18 * practical_marks +
        0.12 * assignment_pct +
        0.10 * attendance +
        0.8 * study_hours +
        np.random.normal(0, 2.8, num_samples)
    )
    final_score = np.clip(final_score, 35.0, 99.5)
    final_score = np.round(final_score, 2)

    # 9. Performance Category Target
    # Distinction >= 85, First Class >= 70, Second Class >= 55, Remedial < 55
    categories = []
    risk_levels = []
    for s in final_score:
        if s >= 85.0:
            categories.append("Distinction")
            risk_levels.append("Low")
        elif s >= 70.0:
            categories.append("First Class")
            risk_levels.append("Low")
        elif s >= 55.0:
            categories.append("Second Class")
            risk_levels.append("Medium")
        else:
            categories.append("Remedial")
            risk_levels.append("High")

    df = pd.DataFrame({
        "previous_semester_marks": np.round(prev_marks, 1),
        "attendance_percentage": np.round(attendance, 1),
        "internal_examination_marks": np.round(internal_marks, 1),
        "assignment_completion_pct": np.round(assignment_pct, 1),
        "practical_examination_marks": np.round(practical_marks, 1),
        "classroom_participation": participation,
        "study_hours_per_day": study_hours,
        "final_academic_percentage": final_score,
        "performance_category": categories,
        "academic_risk_level": risk_levels
    })

    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "student_performance_dataset.csv")
    df = generate_dataset()
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples saved to {out_path}")
    print(df.head(5))
