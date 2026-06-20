from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.models.report import Report

my_report = Blueprint("my_report", __name__)
report_model = Report()


@my_report.route("/my-reports")
def my_reports():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth_user.login"))
    
    user_reports = report_model.get_user_reports(user_id)
    return render_template("user/my_report.html", reports=user_reports)


@my_report.route("/delete_report", methods=["POST"])
def delete_report():
    user_id = session.get("user_id")
    report_id = request.form.get("report_id")
    report_data = report_model.find_by_id(report_id)

    if report_data and report_data['user_id'] == user_id:
        report_model.delete_by_id(report_id)

    return redirect(url_for('my_report.my_reports'))

@my_report.route("/update_report_status/<int:report_id>", methods=["POST"])
def update_report_status(report_id):
    if session.get("user_role") != 'admin':
        return jsonify({"success": False, "error": "Only admins can update status"}), 403
    
    status = request.form.get("status")
    
    if report_model.update_status(report_id, status):
        return jsonify({"success": True}), 200
    
    return jsonify({"success": False}), 500

@my_report.route("/edit_report/<int:report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_auth.login"))

    report_data = report_model.find_by_id(report_id)

    if not report_data or report_data['user_id'] != user_id:
        return redirect(url_for('my_report.my_reports'))

    if request.method == "POST":
        location = request.form.get("location")
        waste_type = request.form.get("waste_type")
        description = request.form.get("description")
        image_file = request.files.get("image")

        report_model.update_report(report_id, location, waste_type, description, image_file)
        return redirect(url_for('my_report.my_reports'))

    return render_template("user/edit_report.html", report=report_data)