from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.report import Report

my_report = Blueprint("my_report", __name__)
report_model = Report()


@my_report.route("/my-reports")
@login_required
def my_reports():
    """
    Display all reports submitted by the current user.
    Only authenticated users can access this page.
    """
    user_reports = report_model.get_user_reports(current_user.id)
    return render_template("user/my_reports.html", reports=user_reports)