import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.report import Report

my_reportBP = Blueprint("my_report", __name__)

@my_reportBP.route("/my_report")
def my_report():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    report = Report()
    reports = report.get_user_reports(session['user_id'])
    return render_template("user/my_report.html", reports=reports)


@my_reportBP.route("/my_report/delete", methods=['POST'])
def delete_report():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    report_id = request.form.get('report_id')
    report = Report()

    # Get the report first to find the image path
    existing = report.find_by_id(report_id)

    # Delete image file if it exists
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
def edit_report(report_id):
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

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