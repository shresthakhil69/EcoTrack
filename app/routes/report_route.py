from flask import Blueprint, render_template, request, current_app, send_from_directory, url_for, redirect
import os
import json
from datetime import datetime

report = Blueprint("report", __name__)


@report.route("/reports")
def reports():
    return render_template("user/reports.html")


def _reports_data_path():
    """Return path to the reports JSON file inside app/data/reports.json."""
    data_dir = os.path.join(current_app.root_path, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "reports.json")


def _load_reports():
    path = _reports_data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_reports(reports):
    path = _reports_data_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)


@report.route("/submit_report", methods=["POST"])
def submit_report():

    location = request.form.get("location")
    waste_type = request.form.get("waste_type")
    description = request.form.get("description")

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads"
    )

    os.makedirs(upload_folder, exist_ok=True)

    image = request.files.get("image")
    imagename = None
    if image and image.filename:
        filepath = os.path.join(upload_folder, image.filename)
        image.save(filepath)
        imagename = image.filename

    report_rec = {
        "location": location,
        "waste_type": waste_type,
        "description": description,
        "image": imagename,
        "reported_on": datetime.utcnow().isoformat() + "Z"
    }

    reports_list = _load_reports()
    reports_list.append(report_rec)
    _save_reports(reports_list)

    return render_template("user/report_success.html", filename=imagename)


@report.route("/reports/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(current_app.root_path, "static", "uploads"),
        filename
    )




