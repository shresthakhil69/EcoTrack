from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.report import Report

report = Blueprint("report", __name__)
report_model = Report()

@report.route("/submit_report", methods=["POST"])
@login_required
def submit_report():
    """
    Handle report submission with image upload.
    Only authenticated users can submit reports.
    """
    location = request.form.get("location")
    waste_type = request.form.get("waste_type")
    description = request.form.get("description")
    image = request.files.get("image")

    # Create report linked to current user
    report_id = report_model.create(
        user_id=current_user.id,
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
@login_required
def submit():
    """
    Display the submit report form.
    Only authenticated users can access this page.
    """
    return render_template("user/reports.html")