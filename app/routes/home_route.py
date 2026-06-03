from flask import Blueprint, render_template, session, redirect, url_for

home = Blueprint("home", __name__)

@home.route("/")
def index():
    return render_template("home.html")

@home.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("user/dashboard.html")