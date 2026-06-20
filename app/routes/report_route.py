from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.report import Report

report = Blueprint("report", __name__)
report_model = Report()

@report.route("/submit_report", methods=["POST"])
def submit_report():
    from app.controller.reports_controller import submit_report_controller
    return submit_report_controller()

@report.route("/submit")
def submit():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_auth.login"))
    
    return render_template("user/reports.html")