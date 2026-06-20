from flask import Blueprint, render_template, session
# from app.models.admin_report import Report

dashboardBP = Blueprint("dashboard", __name__)

@dashboardBP.route("/dashboard")
def dashboard():
    return render_template("user/dashboard.html")