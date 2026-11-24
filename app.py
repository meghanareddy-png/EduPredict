"""
EduPredict - AI-Powered Student Academic Performance Prediction and Monitoring System
Tagline: "Predict. Perform. Progress."

Main Flask Application Entry Point
"""

import os
from flask import Flask, render_template, session, redirect, url_for, g
from config import Config
from models import db
from database.seed import seed_database
from routes.auth import auth_bp
from routes.student import student_bp
from routes.parent import parent_bp
from routes.faculty import faculty_bp
from routes.admin import admin_bp
from routes.prediction import prediction_bp
from routes.helpers import get_current_user

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(parent_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(prediction_bp)

    # Inject global template context
    @app.context_processor
    def inject_global_variables():
        user = get_current_user()
        unread_notifs = 0
        if user:
            unread_notifs = user.notifications.filter_by(is_read=False).count()

        return {
            "brand": Config.BRAND,
            "current_user": user,
            "unread_notifications_count": unread_notifs,
            "current_year": 2026
        }

    # Homepage / Landing page route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Health check endpoint
    @app.route("/health")
    def health():
        return {"status": "ok", "app": "EduPredict", "version": "2.0"}, 200

    # Ensure DB tables exist & are seeded
    seed_database(app)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "True").lower() in ("true", "1")
    print(f"[EduPredict Server] Running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
