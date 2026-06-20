from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.report import Report

report = Blueprint("report", __name__)
report_model = Report()

@report.route("/submit_report", methods=["POST"])
def submit_report():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_auth.login"))

    location = request.form.get("location")
    waste_type = request.form.get("waste_type")
    description = request.form.get("description")
    image = request.files.get("image")

    report_id = report_model.create(
        user_id=user_id,
        location=location,
        waste_type=waste_type,
        description=description,
        image_file=image
    )

    if report_id:
        return render_template("user/report_success.html", report_id=report_id)
    else:
        return "Error saving report", 500

@report.route("/submit")
def submit():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("user_auth.login"))
    
    return render_template("user/reports.html")