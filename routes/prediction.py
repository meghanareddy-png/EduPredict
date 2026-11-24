"""
Prediction API Endpoints
"""

from flask import Blueprint, request, jsonify
from ml.predict import predict_student_performance, simulate_future_score, get_model_metadata

prediction_bp = Blueprint("prediction", __name__, url_prefix="/api/prediction")

@prediction_bp.route("/predict", methods=["POST"])
def run_predict():
    data = request.get_json() or {}
    try:
        res = predict_student_performance(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@prediction_bp.route("/simulate", methods=["POST"])
def run_simulate():
    data = request.get_json() or {}
    baseline = data.get("baseline", {})
    hypothetical = data.get("hypothetical", {})
    try:
        res = simulate_future_score(baseline, hypothetical)
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@prediction_bp.route("/model-info", methods=["GET"])
def model_info():
    return jsonify(get_model_metadata())
