"""
EduPredict Machine Learning Inference & Recommendation Engine
Provides:
- Model inference (Regression score, Category, Risk Level)
- Feature weakness detection
- Personalized, actionable pedagogical recommendations
- Future Score Simulator computation
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "model_artifacts")

_REGRESSOR = None
_CAT_CLASSIFIER = None
_RISK_CLASSIFIER = None
_SCALER = None
_METADATA = None

FEATURE_NAMES = [
    "previous_semester_marks",
    "attendance_percentage",
    "internal_examination_marks",
    "assignment_completion_pct",
    "practical_examination_marks",
    "classroom_participation",
    "study_hours_per_day"
]

def load_models():
    global _REGRESSOR, _CAT_CLASSIFIER, _RISK_CLASSIFIER, _SCALER, _METADATA
    if _REGRESSOR is None:
        reg_path = os.path.join(ARTIFACTS_DIR, "regressor.joblib")
        cat_path = os.path.join(ARTIFACTS_DIR, "cat_classifier.joblib")
        risk_path = os.path.join(ARTIFACTS_DIR, "risk_classifier.joblib")
        scaler_path = os.path.join(ARTIFACTS_DIR, "scaler.joblib")
        meta_path = os.path.join(ARTIFACTS_DIR, "metadata.json")

        if not os.path.exists(reg_path):
            from ml.train_model import train_and_save_models
            train_and_save_models()

        _REGRESSOR = joblib.load(reg_path)
        _CAT_CLASSIFIER = joblib.load(cat_path)
        _RISK_CLASSIFIER = joblib.load(risk_path)
        _SCALER = joblib.load(scaler_path)

        with open(meta_path, "r") as f:
            _METADATA = json.load(f)

def predict_student_performance(features: dict) -> dict:
    """
    Computes expected marks, performance category, risk level,
    weak areas, and tailored recommendations.
    """
    load_models()

    prev_marks = float(features.get("previous_semester_marks", 70.0))
    attendance = float(features.get("attendance_percentage", 75.0))
    internal = float(features.get("internal_examination_marks", 65.0))
    assignment = float(features.get("assignment_completion_pct", 70.0))
    practical = float(features.get("practical_examination_marks", 70.0))
    participation = float(features.get("classroom_participation", 6.0))
    study_hours = float(features.get("study_hours_per_day", 2.5))

    vector = pd.DataFrame([{
        "previous_semester_marks": prev_marks,
        "attendance_percentage": attendance,
        "internal_examination_marks": internal,
        "assignment_completion_pct": assignment,
        "practical_examination_marks": practical,
        "classroom_participation": participation,
        "study_hours_per_day": study_hours
    }], columns=FEATURE_NAMES)

    # 1. Regression Score
    pred_score = float(_REGRESSOR.predict(vector)[0])
    pred_score = round(min(99.5, max(30.0, pred_score)), 2)

    # 2. Performance Category
    pred_cat = str(_CAT_CLASSIFIER.predict(vector)[0])

    # 3. Risk Level
    vector_scaled = _SCALER.transform(vector)
    pred_risk = str(_RISK_CLASSIFIER.predict(vector_scaled)[0])

    # Weak areas detection
    weak_areas = []
    if attendance < 75.0:
        weak_areas.append(f"Low Attendance ({attendance}% < 75% requirement)")
    if internal < 60.0:
        weak_areas.append(f"Sub-optimal Internal Marks ({internal}%)")
    if assignment < 70.0:
        weak_areas.append(f"Lagging Assignment Completion ({assignment}%)")
    if practical < 60.0:
        weak_areas.append(f"Practical Lab Score ({practical}%)")
    if study_hours < 2.0:
        weak_areas.append(f"Low Daily Study Time ({study_hours} hrs/day)")
    if not weak_areas:
        weak_areas.append("Balanced performance across academic indicators")

    # Personalized recommendations
    recommendations = []
    if attendance < 75.0:
        recommendations.append("Prioritize attending all remaining lecture hours to eliminate attendance shortage.")
    if internal < 60.0:
        recommendations.append("Review core textbook problem sets and attend faculty office hours for difficult concepts.")
    if assignment < 75.0:
        recommendations.append("Complete and submit upcoming assignments before deadlines to recover coursework marks.")
    if study_hours < 3.0:
        recommendations.append("Dedicate at least 1.5 to 2 additional focused study hours daily in quiet study intervals.")
    if pred_risk == "High":
        recommendations.append("Schedule an urgent 1-on-1 mentorship session with your class faculty advisor.")
    elif pred_risk == "Medium":
        recommendations.append("Participate in peer study circles and clear conceptual doubts early.")
    else:
        recommendations.append("Maintain your consistent study routine and explore advanced technical electives.")

    return {
        "success": True,
        "predicted_percentage": pred_score,
        "performance_category": pred_cat,
        "risk_level": pred_risk,
        "weak_areas": "; ".join(weak_areas),
        "recommendations": " | ".join(recommendations),
        "recommendations_list": recommendations,
        "input_features": features,
        "model_version": _METADATA.get("version", "v1.0-scikit-ensemble") if _METADATA else "v1.0"
    }

def simulate_future_score(baseline: dict, hypothetical: dict) -> dict:
    """
    Future Score Simulator:
    Computes baseline vs. hypothetical trajectory and returns difference metrics.
    """
    base_res = predict_student_performance(baseline)

    # In hypothetical scenario, simulate synergy
    hypo_features = baseline.copy()
    hypo_features.update(hypothetical)

    hypo_res = predict_student_performance(hypo_features)

    delta = round(hypo_res["predicted_percentage"] - base_res["predicted_percentage"], 2)

    return {
        "success": True,
        "is_hypothetical": True,
        "baseline": base_res,
        "hypothetical": hypo_res,
        "score_difference": delta,
        "improved": delta > 0,
        "notice": "Simulated estimates are generated for educational planning and are not guaranteed examination results."
    }

def get_model_metadata() -> dict:
    load_models()
    return _METADATA or {}
