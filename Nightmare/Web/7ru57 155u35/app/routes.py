from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.register"))

    return render_template(
        "dashboard.html",
        username=session.get("username")
    )

# ✅ robots.txt route
@main_bp.route("/robots.txt")
def robots():
    return send_from_directory(
        os.path.dirname(os.path.dirname(__file__)),
        "robots.txt",
        mimetype="text/plain"
    )
