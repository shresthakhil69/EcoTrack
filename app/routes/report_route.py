from flask import Blueprint, render_template
from app.models.report import Report
from app.auth import login_required

report = Blueprint("report", __name__)
report_model = Report()

@report.route("/submit_report", methods=["POST"])
@login_required
def submit_report():
    from app.controller.reports_controller import submit_report_controller
    return submit_report_controller()

@report.route("/submit")
@login_required
def submit():
    return render_template("user/reports.html")