from flask import Blueprint, render_template, request
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

@my_report.route("/delete_report/<int:report_id>", methods=["POST"])
@login_required
def delete_report(report_id):
    """
    Delete a report by ID.
    Only the report owner can delete their own report.
    """
    report_data = report_model.find_by_id(report_id)
    
    # Check if user owns this report
    if report_data and report_data['user_id'] == current_user.id:
        if report_model.delete_by_id(report_id):
            return {"success": True}, 200
    
    return {"success": False}, 403

@my_report.route("/update_report_status/<int:report_id>", methods=["POST"])
@login_required
def update_report_status(report_id):
    """
    Update the status of a report.
    Only admin users can update report status.
    """
    if current_user.role != 'admin':
        return {"success": False, "error": "Only admins can update status"}, 403
    
    status = request.form.get("status")
    
    if report_model.update_status(report_id, status):
        return {"success": True}, 200
    
    return {"success": False}, 500