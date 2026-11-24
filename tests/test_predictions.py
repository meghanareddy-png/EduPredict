"""
Automated Unit Tests for Machine Learning Inference and Simulator
"""

import pytest
from app import create_app
from config import TestConfig
from ml.predict import predict_student_performance, simulate_future_score, get_model_metadata

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_ml_prediction_inference():
    sample_features = {
        "previous_semester_marks": 78.5,
        "attendance_percentage": 82.0,
        "internal_examination_marks": 75.0,
        "assignment_completion_pct": 88.0,
        "practical_examination_marks": 80.0,
        "classroom_participation": 7.5,
        "study_hours_per_day": 3.0
    }
    result = predict_student_performance(sample_features)
    assert result["success"] is True
    assert 30.0 <= result["predicted_percentage"] <= 100.0
    assert result["performance_category"] in ["Distinction", "First Class", "Second Class", "Remedial"]
    assert result["risk_level"] in ["Low", "Medium", "High"]
    assert len(result["recommendations_list"]) > 0
    assert "weak_areas" in result

def test_high_risk_prediction():
    struggling_features = {
        "previous_semester_marks": 42.0,
        "attendance_percentage": 52.0,
        "internal_examination_marks": 45.0,
        "assignment_completion_pct": 40.0,
        "practical_examination_marks": 50.0,
        "classroom_participation": 3.0,
        "study_hours_per_day": 1.0
    }
    result = predict_student_performance(struggling_features)
    assert result["success"] is True
    assert result["risk_level"] in ["High", "Medium"]
    assert "Low Attendance" in result["weak_areas"]
    assert any("mentorship" in rec or "attendance" in rec.lower() for rec in result["recommendations_list"])

def test_future_score_simulator():
    baseline = {
        "previous_semester_marks": 60.0,
        "attendance_percentage": 68.0,
        "internal_examination_marks": 58.0,
        "assignment_completion_pct": 65.0,
        "practical_examination_marks": 60.0,
        "classroom_participation": 5.0,
        "study_hours_per_day": 2.0
    }
    hypothetical = {
        "attendance_percentage": 92.0,
        "internal_examination_marks": 82.0,
        "assignment_completion_pct": 95.0,
        "study_hours_per_day": 4.5
    }
    sim_result = simulate_future_score(baseline, hypothetical)
    assert sim_result["success"] is True
    assert sim_result["is_hypothetical"] is True
    assert "score_difference" in sim_result
    # Improving attendance, internals and study hours should yield a positive score delta
    assert sim_result["score_difference"] > 0
    assert sim_result["improved"] is True
    assert "estimates are generated for educational planning" in sim_result["notice"]

def test_api_predict_endpoint(client):
    payload = {
        "previous_semester_marks": 72.0,
        "attendance_percentage": 80.0,
        "internal_examination_marks": 70.0,
        "assignment_completion_pct": 85.0,
        "practical_examination_marks": 75.0,
        "classroom_participation": 7.0,
        "study_hours_per_day": 3.0
    }
    res = client.post("/api/prediction/predict", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "predicted_percentage" in data

def test_api_simulate_endpoint(client):
    payload = {
        "baseline": {
            "previous_semester_marks": 65.0,
            "attendance_percentage": 70.0,
            "internal_examination_marks": 62.0,
            "assignment_completion_pct": 70.0,
            "practical_examination_marks": 65.0,
            "classroom_participation": 6.0,
            "study_hours_per_day": 2.5
        },
        "hypothetical": {
            "attendance_percentage": 88.0,
            "internal_examination_marks": 80.0,
            "assignment_completion_pct": 95.0,
            "study_hours_per_day": 4.0
        }
    }
    res = client.post("/api/prediction/simulate", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["is_hypothetical"] is True
    assert data["score_difference"] > 0
