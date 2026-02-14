import re
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

# --------------------
# Forms
# --------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=3, max=50)]
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

# --------------------
# Routes
# --------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data

        # Strong input validation (no XSS / SSTI)
        if not USERNAME_REGEX.match(username):
            return render_template("register.html", form=form, error="Invalid username")

        # Create session (INTENDED VULN LIVES HERE)
        session.clear()
        session["username"] = username
        session["is_admin"] = False

        return redirect(url_for("main.dashboard"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data

        # Login only works if user already registered in session
        if session.get("username") != username:
            return render_template(
                "login.html",
                form=form,
                error="Invalid credentials"
            )

        return redirect(url_for("main.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
