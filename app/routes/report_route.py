from flask import Blueprint, render_template, request, current_app, send_from_directory
import os

report = Blueprint("report", __name__)

@report.route("/reports")
def reports():
    return render_template("user/reports.html")

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
    if image:
        filepath = os.path.join(
            upload_folder,
            image.filename
        )

        image.save(filepath)
        imagename = image.filename

    print(f"Location: {location}")
    print(f"Waste Type: {waste_type}")
    print(f"Description: {description}")

    return render_template("user/report_success.html", filename=imagename)

@report.route("/reports/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(current_app.root_path, "static", "uploads"),
        filename
    )

