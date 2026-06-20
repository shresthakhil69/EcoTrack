import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.auth import login_required
from app.models.report import Report

my_reportBP = Blueprint("my_report", __name__)

@my_reportBP.route("/my_report")
@login_required
def my_report():
    report = Report()
    reports = report.get_user_reports(session['user_id'])
    return render_template("user/my_report.html", reports=reports)


@my_reportBP.route("/my_report/delete", methods=['POST'])
@login_required
def delete_report():
    report_id = request.form.get('report_id')
    report = Report()

    existing = report.find_by_id(report_id)

    if existing and existing['image_path']:
        image_full_path = os.path.join(
            os.path.dirname(__file__), '..', 'static', 'uploads', existing['image_path']
        )
        if os.path.exists(image_full_path):
            os.remove(image_full_path)

    report.delete_by_id(report_id)

    flash('Report deleted successfully.', 'success')
    return redirect(url_for('my_report.my_report'))

@my_reportBP.route("/my_report/edit/<int:report_id>", methods=["GET", "POST"])
@login_required
def edit_report(report_id):
    report = Report()
    report_data = report.find_by_id(report_id)

    if not report_data or report_data['user_id'] != session['user_id']:
        return redirect(url_for('my_report.my_report'))

    if request.method == "POST":
        location = request.form.get("location")
        waste_type = request.form.get("waste_type")
        description = request.form.get("description")
        image_file = request.files.get("image")

        report.update_report(report_id, location, waste_type, description, image_file)
        flash('Report updated successfully.', 'success')
        return redirect(url_for('my_report.my_report'))

    return render_template("user/edit_report.html", report=report_data)