from flask import Blueprint, render_template, current_app, url_for, request, redirect, jsonify
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


def _save_reports(reports):
    path = _reports_data_path()
    # ensure data dir exists
    data_dir = os.path.dirname(path)
    os.makedirs(data_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)


@my_report.route('/delete_report', methods=['POST'])
def delete_report():
    """Delete a report by index and return JSON for AJAX or redirect back."""
    idx_val = request.form.get('index')
    try:
        idx = int(idx_val)
    except (TypeError, ValueError):
        return redirect(url_for('my_report.reports'))

    reports_list = _load_reports()
    if idx < 0 or idx >= len(reports_list):
        return redirect(url_for('my_report.reports'))

    report = reports_list.pop(idx)

    # delete image file if present
    img = report.get('image')
    if img:
        img_path = os.path.join(current_app.root_path, 'static', 'uploads', img)
        try:
            if os.path.exists(img_path):
                os.remove(img_path)
        except OSError:
            pass

    _save_reports(reports_list)

    # If AJAX request return JSON; otherwise redirect back
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True})

    return redirect(url_for('my_report.reports'))


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