import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.report import Report

settingBP = Blueprint("setting", __name__)


@settingBP.route("/setting", methods=['GET', 'POST'])
def setting():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    user_id = session['user_id']
    user = User()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # ── Profile Update ──────────────────────────
        if form_type == 'profile':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()

            if not name or not email:
                flash('Name and email are required.', 'error')
                return redirect(url_for('setting.setting'))

            if phone and (not phone.isdigit() or len(phone) != 10):
                flash('Phone number must be exactly 10 digits.', 'error')
                return redirect(url_for('setting.setting'))

            existing = user.get_by_email(email)
            if existing and existing['id'] != user_id:
                flash('That email is already in use by another account.', 'error')
                return redirect(url_for('setting.setting'))

            user.update_profile(user_id, name, email, phone)
            session['user_name'] = name
            session['user_email'] = email
            flash('Profile updated successfully.', 'success')

        # ── Profile Picture Upload ──────────────────
        elif form_type == 'profile_picture':
            file = request.files.get('profile_picture')

            if not file or file.filename == '':
                flash('Please choose an image to upload.', 'error')
                return redirect(url_for('setting.setting'))

            allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
            ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''

            if ext not in allowed_extensions:
                flash('Only PNG, JPG, JPEG or WEBP images are allowed.', 'error')
                return redirect(url_for('setting.setting'))

            upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(f"profile_{user_id}_{file.filename}")
            file.save(os.path.join(upload_folder, filename))

            # Remove old picture if it exists
            old_data = user.get_by_id(user_id)
            if old_data and old_data.get('profile_picture'):
                old_path = os.path.join(upload_folder, old_data['profile_picture'])
                if os.path.exists(old_path):
                    os.remove(old_path)

            user.update_profile_picture(user_id, filename)
            session['profile_picture'] = filename
            flash('Profile picture updated successfully.', 'success')

        # ── Password Change ─────────────────────────
        elif form_type == 'password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            if not current_password or not new_password or not confirm_password:
                flash('All password fields are required.', 'error')
                return redirect(url_for('setting.setting'))

            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return redirect(url_for('setting.setting'))

            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return redirect(url_for('setting.setting'))

            user_data = user.get_by_id(user_id)
            if not user.check_password(user_data['password'], current_password):
                flash('Current password is incorrect.', 'error')
                return redirect(url_for('setting.setting'))

            user.update_password(user_id, new_password)
            flash('Password updated successfully.', 'success')

        # ── Appearance ──────────────────────────────
        # elif form_type == 'appearance':
        #     dark_mode = 1 if request.form.get('dark_mode') == 'on' else 0
        #     user.update_dark_mode(user_id, dark_mode)
        #     session['dark_mode'] = dark_mode
        #     flash('Appearance saved.', 'success')
        elif form_type == 'appearance':
            dark_mode = 1 if request.form.get('dark_mode') == 'on' else 0
            session['dark_mode'] = dark_mode
            flash('Appearance saved.', 'success')

        # ── Delete All Reports ──────────────────────
        elif form_type == 'delete_reports':
            report = Report()
            user_reports = report.get_user_reports(user_id)
            for r in user_reports:
                report.delete_by_id(r['id'])
            flash('All your reports have been deleted.', 'success')

        # ── Delete Account ──────────────────────────
        elif form_type == 'delete_account':
            report = Report()
            user_reports = report.get_user_reports(user_id)
            for r in user_reports:
                report.delete_by_id(r['id'])
            user.delete_account(user_id)
            session.clear()
            flash('Your account has been deleted.', 'success')
            return redirect(url_for('user_auth.login'))

        return redirect(url_for('setting.setting'))

    # On GET — load user data but don't overwrite dark_mode session
    user_data = user.get_by_id(user_id)
    if 'dark_mode' not in session:
        session['dark_mode'] = 0
    if user_data and user_data.get('profile_picture'):
        session['profile_picture'] = user_data['profile_picture']

    return render_template("user/setting.html", user_data=user_data)