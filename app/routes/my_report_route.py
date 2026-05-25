from flask import Blueprint, render_template, current_app, url_for
import os
import json

my_report = Blueprint("my_report", __name__)


def _reports_data_path():
    data_dir = os.path.join(current_app.root_path, "data")
    return os.path.join(data_dir, "reports.json")


def _load_reports():
    path = _reports_data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@my_report.route("/my-reports")
def reports():
    """Render the my_report page and pass saved reports.

    Each report is a dict with keys: location, waste_type, description, image,
    reported_on. The template will iterate over the list and render each
    report's image (if provided) using url_for('static', filename='uploads/<name>').
    """
    reports_list = _load_reports()

    # For compatibility with previous template logic that expected an `uploads`
    # variable, build an uploads list with the images from reports (if any).
    uploads = [r.get('image') for r in reports_list if r.get('image')]

    return render_template("user/my_report.html", uploads=uploads, reports=reports_list)