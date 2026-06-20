import os
from flask import request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.model.reports import Report

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def submit_report_controller():
    user_id = session.get('user_id')

    waste_type = request.form.get('waste_type', '').strip()
    location = request.form.get('location', '').strip()
    description = request.form.get('description', '').strip()

    if not waste_type or not location:
        flash('Waste type and location are required.', 'error')
        return redirect(url_for('reports.reports'))

    # Handle image upload
    image_path = None
    file = request.files.get('image')
    if file and file.filename != '' and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image_path = filename

    # Save report
    report = Report(
        user_id=user_id,
        waste_type=waste_type,
        description=description,
        location=location,
        image_path=image_path
    )
    report.save()

    flash('Report submitted successfully!', 'success')
    return redirect(url_for('report_success.report_success'))
