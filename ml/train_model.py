"""
EduPredict Machine Learning Training Pipeline
Trains:
1. RandomForestRegressor -> expected academic percentage (R², MAE, RMSE)
2. DecisionTreeClassifier -> performance category ('Distinction', 'First Class', 'Second Class', 'Remedial')
3. LogisticRegression -> academic risk level ('Low', 'Medium', 'High')
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_recall_fscore_support
)

from ml.generate_dataset import generate_dataset

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "model_artifacts")

FEATURE_COLUMNS = [
    "previous_semester_marks",
    "attendance_percentage",
    "internal_examination_marks",
    "assignment_completion_pct",
    "practical_examination_marks",
    "classroom_participation",
    "study_hours_per_day"
]

def train_and_save_models():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    dataset_path = os.path.join("data", "student_performance_dataset.csv")
    if not os.path.exists(dataset_path):
        print("[EduPredict ML] Generating student performance dataset...")
        df = generate_dataset()
        df.to_csv(dataset_path, index=False)
    else:
        df = pd.read_csv(dataset_path)

    X = df[FEATURE_COLUMNS]
    y_reg = df["final_academic_percentage"]
    y_cat = df["performance_category"]
    y_risk = df["academic_risk_level"]

    # 80/20 train/test split
    X_train, X_test, y_reg_train, y_reg_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    _, _, y_cat_train, y_cat_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)
    _, _, y_risk_train, y_risk_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Random Forest Regressor
    print("[EduPredict ML] Training Random Forest Regressor...")
    regressor = RandomForestRegressor(n_estimators=120, max_depth=12, random_state=42, n_jobs=-1)
    regressor.fit(X_train, y_reg_train)
    y_reg_pred = regressor.predict(X_test)

    r2 = r2_score(y_reg_test, y_reg_pred)
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    rmse = np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))

    print(f"  Regressor Metrics -> R2: {r2:.4f}, MAE: {mae:.2f}%, RMSE: {rmse:.2f}%")

    # 2. Decision Tree Classifier
    print("[EduPredict ML] Training Decision Tree Classifier...")
    cat_classifier = DecisionTreeClassifier(max_depth=6, random_state=42)
    cat_classifier.fit(X_train, y_cat_train)
    y_cat_pred = cat_classifier.predict(X_test)

    cat_acc = accuracy_score(y_cat_test, y_cat_pred)
    cat_prec, cat_rec, cat_f1, _ = precision_recall_fscore_support(y_cat_test, y_cat_pred, average="weighted", zero_division=0)
    print(f"  Category Classifier -> Accuracy: {cat_acc:.4f}, F1: {cat_f1:.4f}")

    # 3. Logistic Regression for Risk Classification
    print("[EduPredict ML] Training Logistic Regression Risk Classifier...")
    risk_classifier = LogisticRegression(max_iter=500, random_state=42)
    risk_classifier.fit(X_train_scaled, y_risk_train)
    y_risk_pred = risk_classifier.predict(X_test_scaled)

    risk_acc = accuracy_score(y_risk_test, y_risk_pred)
    risk_prec, risk_rec, risk_f1, _ = precision_recall_fscore_support(y_risk_test, y_risk_pred, average="weighted", zero_division=0)
    print(f"  Risk Classifier -> Accuracy: {risk_acc:.4f}, F1: {risk_f1:.4f}")

    # Save artifacts
    joblib.dump(regressor, os.path.join(ARTIFACTS_DIR, "regressor.joblib"))
    joblib.dump(cat_classifier, os.path.join(ARTIFACTS_DIR, "cat_classifier.joblib"))
    joblib.dump(risk_classifier, os.path.join(ARTIFACTS_DIR, "risk_classifier.joblib"))
    joblib.dump(scaler, os.path.join(ARTIFACTS_DIR, "scaler.joblib"))

    # Feature Importances
    importances = dict(zip(FEATURE_COLUMNS, [round(float(v), 4) for v in regressor.feature_importances_]))

    metadata = {
        "version": "v1.0-scikit-ensemble",
        "trained_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "features": FEATURE_COLUMNS,
        "feature_importances": importances,
        "metrics": {
            "regression": {
                "algorithm": "Random Forest Regressor (120 trees)",
                "r2_score": round(float(r2), 4),
                "mae": round(float(mae), 2),
                "rmse": round(float(rmse), 2)
            },
            "performance_classification": {
                "algorithm": "Decision Tree Classifier",
                "accuracy": round(float(cat_acc), 4),
                "f1_score": round(float(cat_f1), 4)
            },
            "risk_classification": {
                "algorithm": "Multinomial Logistic Regression",
                "accuracy": round(float(risk_acc), 4),
                "f1_score": round(float(risk_f1), 4)
            }
        }
    }

    with open(os.path.join(ARTIFACTS_DIR, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print("[EduPredict ML] All models & metadata successfully saved to:", ARTIFACTS_DIR)
    return metadata

if __name__ == "__main__":
    train_and_save_models()
