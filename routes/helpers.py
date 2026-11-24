"""
Route Helpers - Authentication Decorators & Utilities
"""

from functools import wraps
from flask import session, redirect, url_for, flash, abort, jsonify
from models import db
from models.user import User

def get_current_user():
    """Retrieves authenticated user object from session or None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please sign in first.", "warning")
                return redirect(url_for("auth.login"))
            
            user_role = session.get("role")
            if user_role not in allowed_roles:
                flash(f"Unauthorized. Access restricted to: {', '.join(allowed_roles)}.", "danger")
                # Redirect to appropriate home dashboard
                if user_role == "student":
                    return redirect(url_for("student.dashboard"))
                elif user_role == "parent":
                    return redirect(url_for("parent.dashboard"))
                elif user_role == "faculty":
                    return redirect(url_for("faculty.dashboard"))
                elif user_role == "admin":
                    return redirect(url_for("admin.dashboard"))
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
